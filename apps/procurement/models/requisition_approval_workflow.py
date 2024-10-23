from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.organization.models import Staff, Unit, Department
from apps.procurement.models.requisition import Requisition, ApprovalChoices


class ApprovalStep(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField()  # to determine step order
    role = models.CharField(
        max_length=255, help_text="Role required for this approval step"
    )
    officer = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    is_optional = models.BooleanField(default=False)  # optional approval steps
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True
    )
    remarks = models.TextField(null=True, blank=True, default="", max_length=1_000)
    is_final = models.BooleanField(default=False)
    time_limit = models.DurationField(
        null=True, blank=True, help_text="Time limit for this approval step"
    )
    description = models.TextField(null=True, blank=True, default="", max_length=1_000)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def workflow(self) -> "ApprovalWorkflow":
        return ApprovalWorkflow.objects.filter(steps=self).get()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "-id"]


class ApprovalWorkflow(models.Model):
    name = models.CharField(max_length=255)
    officer = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    steps = models.ManyToManyField(
        ApprovalStep, related_name="workflows", through="WorkflowStep"
    )
    description = models.TextField(null=True, blank=True, default="", max_length=1_000)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def approval_steps(self, **filter_kwargs) -> list["ApprovalStep"]:
        return self.steps.filter(**filter_kwargs)  # type: ignore

    def workflow_steps(self) -> list["WorkflowStep"]:
        return self.workflowstep_set.filter()  # type: ignore

    def move_to_next_step(self, requisition: Requisition):
        current_step = requisition.current_approval_step
        if current_step:
            next_step = self.workflowstep_set.filter(order__gt=current_step.order).first()  # type: ignore
            if next_step:
                requisition.current_approval_step = next_step
                requisition.save()
                return next_step
        requisition.approval_status = ApprovalChoices.APPROVED
        requisition.current_approval_step = None
        requisition.save()

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE)
    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    order = models.IntegerField()
    condition = models.TextField(
        blank=True, null=True, help_text="Python code for conditional execution"
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        unique_together = ["workflow", "order"]

    def __str__(self):
        return f"{self.workflow.name} - Step {self.order}: {self.step.name}"


class ApprovalMatrix(models.Model):
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE)
    min_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.SET_NULL
    )
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def matches_requisition(self, requisition: Requisition):
        # Check if the requisition matches this matrix row
        if self.min_amount and requisition.total_price < self.min_amount:
            return False
        if self.max_amount and requisition.total_price > self.max_amount:
            return False
        if self.department and requisition.officer_department != self.department:
            return False
        if self.unit and requisition.officer.unit != self.unit:
            return False
        return True

    def __str__(self):
        return f"{self.workflow.name} | Matrix | {self.pk}"


class ApprovalAction(models.Model):
    requisition = models.ForeignKey(
        Requisition, on_delete=models.CASCADE, related_name="approval_actions"
    )
    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    approver = models.ForeignKey(Staff, on_delete=models.CASCADE)
    action = models.CharField(
        max_length=20,
        choices=[
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("delegated", "Delegated"),
        ],
    )
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requisition} - {self.step.name} - {self.action}"


class Delegation(models.Model):
    delegator = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="delegated_from"
    )
    delegate = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="delegated_to"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < timezone.now():
            raise ValidationError("Start date cannot be in the past")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.delegator} delegated to {self.delegate} ({self.start_date} to {self.end_date})"


def get_current_approver(requisition: Requisition):
    current_step = requisition.current_approval_step
    if not current_step:
        return None

    role = current_step.role
    department = requisition.officer_department

    # Check for active delegations
    delegations = Delegation.objects.filter(
        delegator__job_title=role,
        delegator__unit__department=department,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
    )

    if delegations.exists():
        delegation = delegations.first()
        if not delegation:
            return None
        return delegation.delegate

    return Staff.objects.filter(job_title=role, unit__department=department).first()


def get_matrix_for_requisition(requisition: Requisition):
    """
    This function returns a single approval matrix that matches the requisition
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            return matrix
    return None  # Handle no matches found (e.g., assign default workflow)


def get_workflow_for_requisition(requisition: Requisition):
    """
    This function returns a workflow that matches the requisition
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            return matrix.workflow
    return None  # Handle no matches found (e.g., assign default workflow)


def get_workflow_list_for_requisition(requisition: Requisition):
    """
    This function returns a list of workflows that match the requisition
    """
    workflows = ApprovalMatrix.objects.all()  # Get all matrix entries
    _workflows = []
    for matrix in workflows:
        if matrix.matches_requisition(requisition):
            _workflows.append(matrix.workflow)
    return _workflows


def get_matrixes_for_requisition(requisition: Requisition):
    """
    This function returns a list of approval matrixes that match the requisition
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    _matrices = []
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            _matrices.append(matrix)
    return _matrices
