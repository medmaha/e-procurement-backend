from django.db import models

from apps.organization.models import Staff, Unit, Department
from apps.procurement.models.pr_approval_workflow import ApprovalWorkflow
from apps.procurement.models.requisition import Requisition


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

    status = models.CharField(default="active", max_length=25, blank=True)
    description = models.TextField(default="", null=True, blank=True, max_length=300)

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
