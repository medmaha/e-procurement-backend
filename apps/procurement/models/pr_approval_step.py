from django.db import models

from apps.organization.models import Staff, Unit, Department
from apps.procurement.models.requisition import Requisition, ApprovalChoices


class ApprovalStep(models.Model):
    """
    Model representing a single step in the approval process.
    """

    name = models.CharField(max_length=255)
    order = models.IntegerField(default=1)  # to determine step order
    role = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        help_text="Role required for this approval step",
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "-created_date"]
