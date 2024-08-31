from django.db import models
from apps.procurement.models.rfq import RFQ
from apps.vendors.models.vendor import Vendor
from apps.vendors.models.rfq_response import RFQResponse
from apps.accounts.models.account import Account
from apps.organization.models.staff import Staff
from apps.core.utilities.text_choices import ApprovalChoices


def negotiation_notes(instance, filename):
    return f"procurement/negotiation/{instance.contract.rfq.unique_id}/{filename}"


class NegotiationAndAwardStatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    AWARDED = "AWARDED", "Awarded"
    SUCCESSFUL = "SUCCESSFUL", "Successful"
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    UNSUCCESSFUL = "UNSUCCESSFUL", "Unsuccessful"
    TERMINATED = "TERMINATED", "Terminated"


class RFQContract(models.Model):

    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name="contracts")
    supplier = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="rfq_contracts"
    )
    rfq_response = models.OneToOneField(
        RFQResponse, on_delete=models.CASCADE, related_name="contract"
    )
    approval_status = models.CharField(
        max_length=100,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING,
    )
    delivery_terms = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    validity_period = models.DateTimeField(null=True, blank=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)

    deadline_date = models.DateTimeField(null=True, blank=True)
    terms_and_conditions = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=NegotiationAndAwardStatusChoices.choices,
        default=NegotiationAndAwardStatusChoices.PENDING,
    )
    officer = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="authored_rfq_contracts"
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class RFQNegotiationNote(models.Model):
    contract = models.ForeignKey(
        RFQContract, on_delete=models.CASCADE, related_name="notification_notes"
    )

    delivery_terms = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    validity_period = models.DateTimeField(null=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)

    accepted = models.BooleanField(default=False)
    renegotiated = models.BooleanField(default=False)

    note = models.TextField()
    file = models.FileField(upload_to=negotiation_notes, null=True, blank=True)
    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="contract_notification_notes"
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RFQ Negotiation Note"
        ordering = ["-created_date", "accepted"]


class RFQNegotiation(models.Model):
    contract = models.ForeignKey(
        RFQContract,
        on_delete=models.CASCADE,
        related_name="negotiation",
    )

    notes = models.ManyToManyField(RFQNegotiationNote, blank=True)
    outcome = models.TextField(default="", blank=True)
    status = models.CharField(
        max_length=50,
        choices=NegotiationAndAwardStatusChoices.choices,
        default=NegotiationAndAwardStatusChoices.PENDING,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class RFQContractAward(models.Model):
    contract = models.ForeignKey(
        RFQContract, on_delete=models.CASCADE, related_name="awards"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="rfq_contract_awards"
    )
    officer = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="authored_rfq_awards"
    )

    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=NegotiationAndAwardStatusChoices.choices,
        default=NegotiationAndAwardStatusChoices.PENDING,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class RFQContractApproval(models.Model):
    contract = models.OneToOneField(
        RFQContract,
        on_delete=models.CASCADE,
        related_name="approval_record",
    )
    approve = models.CharField(
        max_length=50,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING,
    )
    editable = models.BooleanField(default=True, blank=True, null=False)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        ordering = ["-id"]
