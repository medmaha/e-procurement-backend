from django.db import models
from apps.organization.models.staff import Staff
from apps.core.utilities.text_choices import ApprovalChoices


class UnitRequisitionApproval(models.Model):
    """
    This is the department where requisition was issued
    * The department and unit heads will have approved this requisition
    """

    parent_id = models.CharField(max_length=255)
    officer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="unit_approval_officer",
    )
    approve = models.CharField(
        default="no",
        max_length=255,
        choices=ApprovalChoices.choices,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    remark = models.TextField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.approve.upper()
