from django.db import models
from apps.vendors.models.rfq_response import RFQResponse
from apps.accounts.models.account import Account
from apps.organization.models.staff import Staff
from apps.core.utilities.text_choices import ApprovalChoices


class ContractAwardStatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    AWARDED = "AWARDED", "Awarded"
    REJECTED = "REJECTED", "Rejected"


class ContractAward(models.Model):
    quotation = models.OneToOneField(RFQResponse, on_delete=models.CASCADE)

    officer = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
    )

    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=50,
        choices=ContractAwardStatusChoices.choices,
        default=ContractAwardStatusChoices.PENDING,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def has_create_perm(cls, user: Account):
        """Check if the user has the permission to create the model."""
        return user.has_perm(f"{cls._meta.app_label}.add_{cls._meta.model_name}")


class ContractAwardApproval(models.Model):
    approver = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
    )
    award = models.OneToOneField(
        ContractAward, on_delete=models.CASCADE, related_name="approval"
    )

    remarks = models.TextField(blank=True, null=True)

    approve = models.CharField(
        max_length=50,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING,
    )

    created_date = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    @classmethod
    def has_create_perm(cls, user: Account):
        """Check if the user has the permission to create the model."""
        return user.has_perm(f"{cls._meta.app_label}.add_{cls._meta.model_name}")

    def has_update_perm(self, user: Account):
        """Check if the user has update permission for the model."""
        return user.has_perm(f"{self._meta.app_label}.change_{self._meta.model_name}")

    class Meta:
        ordering = ["-id"]
