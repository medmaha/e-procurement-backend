from django.db import models

from apps.organization.models import Staff
from apps.procurement.models.requisition import Requisition, ApprovalChoices
from .pr_approval_step import ApprovalStep


class ApprovalWorkflow(models.Model):
    """
    Model representing the entire approval workflow.
    """

    name = models.CharField(max_length=255)
    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    steps = models.ManyToManyField(
        ApprovalStep, related_name="workflows", through="WorkflowStep"
    )
    status = models.CharField(
        max_length=255,
        default="active",
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True, default="", max_length=1_000)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def workflow_steps(self):
        """
        Get all workflow steps for this workflow.
        """
        return self.workflowstep_set.filter()  # type: ignore

    def get_initial_step(self, requisition: Requisition):
        from .pr_approval_workflow_step import WorkflowStep

        steps = WorkflowStep.objects.filter(workflow=self)

        for next_step in steps:
            if next_step.check_condition(requisition):
                return next_step

    def move_to_next_step(self, requisition: Requisition):
        """
        Move the requisition to the next applicable approval step or mark as approved.
        """
        current_step = requisition.current_approval_step
        if current_step:
            next_steps = self.workflowstep_set.filter(order__gt=current_step.order)  # type: ignore
            for next_step in next_steps:
                if next_step.check_condition(requisition):
                    requisition.approval_status = ApprovalChoices.PENDING
                    requisition.current_approval_step = next_step
                    requisition.save()
                    return next_step

        from apps.procurement.models import ApprovalAction

        approvals = ApprovalAction.objects.select_related().only("action").filter(requisition=requisition)  # type: ignore

        if not approvals.exists():
            return

        if requisition.approval_actions.count() == 0:  # type: ignore
            return

        # Return if there are still some pending approvals
        pending_approval = approvals.filter(action=ApprovalChoices.PENDING)  # type: ignore
        if pending_approval.exists():
            requisition.approval_status = ApprovalChoices.PENDING
            requisition.current_approval_step = pending_approval.first().workflow_step  # type: ignore
            requisition.save()
            return pending_approval.workflow_step

        # Return if no approval was made for this (PR)
        rejected_approval = approvals.filter(action=ApprovalChoices.REJECTED)  # type: ignore
        if rejected_approval.exists():
            requisition.approval_status = ApprovalChoices.REJECTED
            requisition.current_approval_step = None
            requisition.save()
            return None

        # If no next step or no conditions met, mark as approved
        requisition.approval_status = ApprovalChoices.APPROVED
        requisition.current_approval_step = None
        requisition.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["status", "-created_date"]
