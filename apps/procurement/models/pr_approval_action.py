from django.db import models

from apps.organization.models import Staff
from apps.procurement.models.pr_approval_workflow_step import WorkflowStep
from apps.procurement.models.requisition import Requisition


class ApprovalAction(models.Model):
    """
    Model to record approval actions taken on requisitions.
    """

    requisition = models.ForeignKey(
        Requisition, on_delete=models.CASCADE, related_name="approval_actions"
    )
    workflow_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, null=True)
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
        return f"{self.requisition} - {self.workflow_step.step.name} - {self.action}"

    def move_to_next_step(self):
        self.workflow_step.workflow.move_to_next_step(self.requisition)
