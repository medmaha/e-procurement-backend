from django.db import models
from apps.organization.models.staff import Staff
from apps.procurement.models.rfq import RFQ

from apps.core.utilities.text_choices import ApprovalChoices
from apps.core.utilities.generators import generate_unique_id
from apps.accounts.models.account import Account


class RFQApprovalGPPA(models.Model):
    rfq = models.OneToOneField(
        RFQ,
        blank=True,
        on_delete=models.CASCADE,
        related_name="approval_record_gppa",
    )
    officer = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="approval_officer_gppa"
    )
    approve = models.CharField(
        max_length=100, choices=ApprovalChoices.choices, default=ApprovalChoices.PENDING
    )
    editable = models.BooleanField(default=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)


class RFQApproval(models.Model):
    rfq = models.OneToOneField(
        RFQ,
        blank=True,
        on_delete=models.CASCADE,
        related_name="approval_record",
    )
    gppa_approval = models.ForeignKey(
        RFQApprovalGPPA,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approval_record",
    )
    officer = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, related_name="approval_officer"
    )
    approve = models.CharField(
        max_length=100, choices=ApprovalChoices.choices, default=ApprovalChoices.PENDING
    )
    editable = models.BooleanField(default=True, blank=True)
    remarks = models.TextField(max_length=300, default="", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def unique_id(self):
        return generate_unique_id(None, self.pk)
