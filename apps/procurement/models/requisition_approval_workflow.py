from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.organization.models import Staff, Unit, Department
from apps.procurement.models.requisition import Requisition, ApprovalChoices


class ApprovalStep(models.Model):
    """
    Model representing a single step in the approval process.
    """

    name = models.CharField(max_length=255)
    order = models.IntegerField()  # to determine step order
    role = models.CharField(
        max_length=255, help_text="Role required for this approval step"
    )
    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    approver = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name="approver"
    )
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
        """
        Get the workflow associated with this step.
        """
        return ApprovalWorkflow.objects.filter(steps=self).first()  # type: ignore

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "-id"]


class ApprovalWorkflow(models.Model):
    """
    Model representing the entire approval workflow.
    """

    name = models.CharField(max_length=255)
    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    steps = models.ManyToManyField(
        ApprovalStep, related_name="workflows", through="WorkflowStep"
    )
    description = models.TextField(null=True, blank=True, default="", max_length=1_000)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def approval_steps(self, **filter_kwargs) -> list["ApprovalStep"]:
        """
        Get filtered approval steps for this workflow.
        """
        return self.steps.filter(**filter_kwargs)  # type: ignore

    def workflow_steps(self) -> list["WorkflowStep"]:
        """
        Get all workflow steps for this workflow.
        """
        return self.workflowstep_set.filter()  # type: ignore

    def move_to_next_step(self, requisition: Requisition):
        """
        Move the requisition to the next applicable approval step or mark as approved.
        """
        current_step = requisition.current_approval_step
        if current_step:
            next_steps = self.workflowstep_set.filter(order__gt=current_step.order)  # type: ignore
            for next_step in next_steps:
                if next_step.check_condition(requisition):
                    requisition.current_approval_step = next_step
                    requisition.save()
                    return next_step
        # If no next step or no conditions met, mark as approved
        requisition.approval_status = ApprovalChoices.APPROVED
        requisition.current_approval_step = None
        requisition.save()

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    """
    Model representing the connection between ApprovalWorkflow and ApprovalStep.
    """

    class ConditionType(models.TextChoices):
        AMOUNT_GREATER_THAN = "amount_gt", "Amount greater than"
        AMOUNT_LESS_THAN = "amount_lt", "Amount less than"
        DEPARTMENT_EQUALS = "dept_eq", "Department equals"
        UNIT_EQUALS = "unit_eq", "Unit equals"
        ALWAYS = "always", "Always execute"
        # New conditions
        ITEM_COUNT_GREATER_THAN = "item_count_gt", "Item count greater than"
        REQUISITION_TYPE_EQUALS = "req_type_eq", "Requisition type equals"
        DAYS_SINCE_SUBMISSION = "days_since_sub", "Days since submission"

    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE)
    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    order = models.IntegerField()
    condition_type = models.CharField(
        max_length=20, choices=ConditionType.choices, default=ConditionType.ALWAYS
    )
    condition_value = models.CharField(max_length=255, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def check_condition(self, requisition: Requisition) -> bool:
        """
        Check if the condition for this step is met.
        """
        try:
            if self.condition_type == WorkflowStep.ConditionType.ALWAYS:
                return True
            elif self.condition_type == WorkflowStep.ConditionType.AMOUNT_GREATER_THAN:
                return requisition.total_price > Decimal(self.condition_value or "")
            elif self.condition_type == WorkflowStep.ConditionType.AMOUNT_LESS_THAN:
                return requisition.total_price < Decimal(self.condition_value or "")
            elif self.condition_type == WorkflowStep.ConditionType.DEPARTMENT_EQUALS:
                return requisition.officer_department is not None and (
                    str(requisition.officer_department.pk) == self.condition_value
                )
            elif self.condition_type == WorkflowStep.ConditionType.UNIT_EQUALS:
                return str(requisition.officer.unit.pk) == self.condition_value
            # New condition checks
            elif (
                self.condition_type
                == WorkflowStep.ConditionType.ITEM_COUNT_GREATER_THAN
            ):
                return requisition.items.count() > int(self.condition_value or "")
            elif (
                self.condition_type
                == WorkflowStep.ConditionType.REQUISITION_TYPE_EQUALS
            ):
                return requisition.requisition_type == self.condition_value  # type: ignore
            elif (
                self.condition_type == WorkflowStep.ConditionType.DAYS_SINCE_SUBMISSION
            ):
                days_since = (timezone.now() - requisition.submission_date).days  # type: ignore
                return days_since > int(self.condition_value or "")
            return False
        except Exception as e:
            return False

    class Meta:
        ordering = ["order"]
        unique_together = ["workflow", "order"]

    def __str__(self):
        return f"{self.workflow.name} - Step {self.order}: {self.step.name}"


class ApprovalMatrix(models.Model):
    """
    Model for defining approval workflows based on various criteria.
    """

    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
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
        """
        Check if the requisition matches this matrix row.
        """
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
    """
    Model to record approval actions taken on requisitions.
    """

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
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requisition} - {self.step.name} - {self.action}"


class Delegation(models.Model):
    """
    Model to handle temporary delegation of approval authority.
    """

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
        """
        Validate delegation dates.
        """
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < timezone.now():
            raise ValidationError("Start date cannot be in the past")

    def save(self, *args, **kwargs):
        """
        Perform validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.delegator} delegated to {self.delegate} ({self.start_date} to {self.end_date})"


def get_current_approver(requisition: Requisition):
    """
    Get the current approver for a requisition, considering delegations.
    """
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
    Get the first matching approval matrix for a requisition.
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            return matrix
    return None  # Handle no matches found (e.g., assign default workflow)


def get_workflow_for_requisition(requisition: Requisition):
    """
    Get the first matching workflow for a requisition.
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            return matrix.workflow
    return None  # Handle no matches found (e.g., assign default workflow)


def get_workflow_list_for_requisition(requisition: Requisition):
    """
    Get a list of all matching workflows for a requisition.
    """
    workflows = ApprovalMatrix.objects.all()  # Get all matrix entries
    _workflows = []
    for matrix in workflows:
        if matrix.matches_requisition(requisition):
            _workflows.append(matrix.workflow)
    return _workflows


def get_matrixes_for_requisition(requisition: Requisition):
    """
    Get a list of all matching approval matrices for a requisition.
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    _matrices = []
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            _matrices.append(matrix)
    return _matrices
