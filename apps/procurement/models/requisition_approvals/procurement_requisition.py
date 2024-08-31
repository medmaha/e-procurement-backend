from django.db import models

from apps.organization.models.staff import Staff
from apps.organization.models.procurement_plan import PlanItem
from apps.core.utilities.text_choices import ApprovalChoices


class ProcurementRequisitionApproval(models.Model):
    parent_id = models.CharField(max_length=255)
    officer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="procurement_departments_approval_officer",
    )
    approve = models.CharField(
        max_length=255,
        choices=ApprovalChoices.choices,
    )
    part_of_annual_plan = models.BooleanField(default=False)
    annual_procurement_plan = models.ForeignKey(
        PlanItem, on_delete=models.SET_NULL, null=True, blank=True
    )
    remark = models.TextField(blank=True, null=True, max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.approve.upper()

    @property
    def parent(self):
        return self.approval  # type: ignore
