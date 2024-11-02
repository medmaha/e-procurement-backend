from django.db import models
from django.utils import timezone

from apps.core.utilities.text_choices import ApprovalChoices
from apps.vendors.models import Vendor
from apps.accounts.models import Account
from apps.organization.models import Staff
from apps.procurement.models.contract_award import ContractAward


class ContractStatusChoices(models.TextChoices):
    DRAFT = ("Draft", "Draft")
    ACTIVE = ("Active", "Active")
    COMPLETED = ("Completed", "Completed")
    TERMINATED = ("Terminated", "Terminated")
    PENDING_APPROVAL = ("Pending Approval", "Pending Approval")


class Contract(models.Model):
    # Linking the contract to a specific supplier
    supplier = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="contracts"
    )

    # Linking the contract to a possible award
    award = models.OneToOneField(
        ContractAward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract",
    )

    title = models.CharField(max_length=255)  # Title or subject of the contract
    description = models.TextField(
        blank=True, null=True
    )  # Detailed description of the contract scope
    start_date = models.DateField(null=True, blank=True)  # Contract start date
    end_date = models.DateField(null=True, blank=True)  # Contract end date

    status = models.CharField(
        max_length=20,
        choices=ContractStatusChoices.choices,
        default=ContractStatusChoices.DRAFT,
    )

    # Key contract terms
    payment_terms = models.TextField()  # Payment terms for the supplier
    delivery_schedule = models.TextField()  # Delivery or performance schedule

    # Terms and conditions - Full text of terms and conditions
    terms_and_conditions = models.TextField()
    # Does the contract have a confidentiality clause?
    confidentiality_clause = models.BooleanField(default=False)
    # Penalty for breaches
    penalty_clause = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Document management
    attachments = models.ManyToManyField(
        "ContractAttachment", blank=True, related_name="contracts"
    )

    officer = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        blank=True,
        related_name="created_contracts",
    )

    # Tracking updates on approval history
    approved_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_contracts",
    )
    approval_status = models.CharField(
        max_length=100,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING,
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_remarks = models.TextField(null=True, blank=True)

    # Tracking updates on termination history
    terminated_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terminated_contracts",
    )
    terminated_reason = models.TextField(max_length=500, null=True, blank=True)
    terminated_date = models.DateTimeField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def has_create_perm(cls, user: Account):
        """Check if the user has the permission to create the model."""
        return user.has_perm(f"{cls._meta.app_label}.add_{cls._meta.model_name}")

    def approve_contract(self, staff: Staff, remarks: str | None = None):
        """
        Approve the contract, set status to 'Active', and log the approving user and date.
        """
        self.status = ContractStatusChoices.ACTIVE
        self.approved_by = staff
        self.approval_date = timezone.now()
        if remarks:
            self.approval_remarks = remarks
        self.save()

    def terminate_contract(self, staff: Staff, reason: str | None = None):
        """
        Terminate the contract, set status to 'Terminated', and log the reason if provided.
        """
        self.status = ContractStatusChoices.TERMINATED
        self.terminated_by = staff
        self.terminated_date = timezone.now()
        if reason:
            self.terminated_reason = reason
            # ContractTermination.objects.create(contract=self, reason=reason)
        self.save()

    def __str__(self):
        return f"Contract {self.title}"


class ContractAttachment(models.Model):
    """
    Model to manage additional documents related to the contract.
    """

    name = models.CharField(max_length=255)
    document_url = models.CharField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
