from django.db import models
from decimal import Decimal

from apps.core.utilities.generators import generate_unique_id
from apps.procurement.models.purchase_order import PurchaseOrder
from apps.core.utilities.text_choices import PaymentTermsChoices


class Invoice(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal())
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Including tax
    notes = models.TextField(blank=True, default="")

    due_date = models.DateField()
    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    payment_terms = models.CharField(
        max_length=20, choices=PaymentTermsChoices.choices, default="net_30", blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("late", "Late"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )

    @property
    def unique_id(self):
        return generate_unique_id("I", self.pk, 6)

    def __str__(self):
        return (
            f"Invoice {self.unique_id} | Vendor: {self.vendor} | Amount: {self.amount}"
        )
