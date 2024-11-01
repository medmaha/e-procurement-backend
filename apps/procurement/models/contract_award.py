from django.db import models
from apps.procurement.models.rfq import RFQ
from apps.vendors.models.vendor import Vendor
from apps.vendors.models.rfq_response import RFQResponse
from apps.accounts.models.account import Account
from apps.organization.models.staff import Staff
from apps.core.utilities.text_choices import ApprovalChoices


class ContractAwardStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    AWARDED = "AWARDED", "Awarded"
    REJECTED = "REJECTED", "Rejected"


class ContractAward(models.Model):
    quotation = models.ForeignKey(RFQResponse, on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="rfq_contract_awards"
    )
    officer = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="authored_rfq_awards"
    )

    comments = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=50,
        choices=ContractAwardStatusChoices.choices,
        default=ContractAwardStatusChoices.PENDING,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class ContractAwardApproval(models.Model):
    officer = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="rfq_contract_approvals"
    )

    award = models.OneToOneField(
        ContractAward,
        on_delete=models.CASCADE,
        related_name="approval_record",
    )
    remarks = models.TextField(blank=True, null=True)
    approve = models.CharField(
        max_length=50,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING,
    )
    editable = models.BooleanField(default=True, blank=True, null=False)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    @classmethod
    def has_create_perm(cls, user: Account):
        """Check if the user has the permission to create the model."""
        return user.has_perm(f"{cls._meta.app_label}.add_{cls._meta.model_name}")

    def has_update_perm(self, user: Account):
        """Check if the user has update permission for the model."""
        return user.has_perm(f"{self._meta.app_label}.change_{self._meta.model_name}")

    def has_delete_perm(self, user: Account):
        """Check if the user has delete permission for the model."""
        return user.has_perm(f"{self._meta.app_label}.delete_{self._meta.model_name}")

    def has_read_perm(self, user: Account):
        """Check if the user has read permission for the model."""
        return user.has_perm(f"{self._meta.app_label}.view_{self._meta.model_name}")

    class Meta:
        ordering = ["-id"]
