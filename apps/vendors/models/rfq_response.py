from django.db import models
from apps.organization.models.staff import Staff

from apps.vendors.models import Vendor

from apps.core.utilities.generators import generate_unique_id
from apps.core.utilities.text_choices import ApprovalChoices


def upload_proforma(instance, filename):
    vendor = instance.vendor
    path = "vendors/id_%s/quotes/proforma/%s/%s" % (
        vendor.id if vendor else "0",
        instance.unique_id,
        filename.replace(" ", "-"),
    )
    return path


def upload_form101(instance, filename):
    vendor = instance.vendor
    path = "vendors/id_%s/quotes/form101/%s/%s" % (
        vendor.id if vendor else "0",
        instance.unique_id,
        filename.replace(" ", "-"),
    )
    return path


def upload_brochure(instance, filename):
    vendor = instance.rfq_response.vendor
    path = "vendors/id_%s/quotes/brochure/%s/%s" % (
        vendor.id if vendor else "0",
        instance.rfq_response.unique_id,
        filename.replace(" ", "-"),
    )
    return path


class RFQResponseBrochure(models.Model):
    rfq_response = models.ForeignKey("RFQResponse", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_brochure, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class RFQResponse(models.Model):
    "Supplies Send this quote to the [Procuring Organization]"
    rfq = models.ForeignKey(
        "procurement.RFQ", on_delete=models.CASCADE, related_name="responses"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="rfq_responses"
    )

    status = models.CharField(
        default="pending",
        max_length=10,
        choices=ApprovalChoices.choices,
        help_text="Whether vendor accepted this requisition or rejects it",
    )

    proforma = models.FileField(upload_to=upload_proforma, null=True)
    form101 = models.FileField(upload_to=upload_form101, null=True, blank=True)
    brochures = models.ManyToManyField(RFQResponseBrochure, blank=True)

    delivery_terms = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    validity_period = models.CharField(max_length=50)

    remarks = models.TextField(max_length=2500, default="", blank=True)

    approved_date = models.DateField(null=True, blank=True)
    approved_remarks = models.TextField(max_length=2500, null=True, blank=True)
    approved_officer = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, blank=True
    )
    approved_status = models.CharField(
        default="processing",
        max_length=15,
        choices=(
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("processing", "Processing"),
        ),
        help_text="Whether vendor accepted this requisition or rejects it",
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def unique_id(self):
        return generate_unique_id(None, self.pk)

    def __str__(self):
        return "RFQ Response -" + self.unique_id

    class Meta:
        ordering = ["-created_date", "-last_modified"]
        verbose_name = "RFQ Response"
        verbose_name_plural = "RFQ Responses"


PAYMENT_CHOICES = [
    ("NET30", "Net 30 Days"),
    ("NET60", "Net 60 Days"),
    ("NET90", "Net 90 Days"),
    ("COD", "Cash On Delivery"),
    ("OTHER", "Other"),
]

DELIVERY_TERMS_CHOICES = [
    ("EXW", "EXW (Ex Works)"),
    ("FOB", "FOB (Free On Board)"),
    ("CIF", "CIF (Cost, Insurance, and Freight)"),
    ("DDP", "DDP (Delivered Duty Paid)"),
    # Add more choices as needed
]
