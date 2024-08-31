from email.policy import default
from random import choice
from django.db import models

from apps.vendors.models.vendor import Vendor
from apps.vendors.models.rfq_response import RFQResponse
from apps.organization.models.staff import Staff
from apps.procurement.models.rfq import RFQ
from apps.core.utilities.text_choices import ApprovalChoices


class PurchaseOrder(models.Model):
    officer = models.ForeignKey(Staff, on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchase_order"
    )
    rfq = models.ForeignKey(
        RFQ, on_delete=models.CASCADE, related_name="purchase_order"
    )
    rfq_response = models.OneToOneField(RFQResponse, on_delete=models.CASCADE)
    comments = models.TextField(max_length=500, blank=False)

    published = models.BooleanField(default=False)
    auto_publish = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=True)
    approval_status = models.CharField(
        max_length=100, default=ApprovalChoices.PENDING, choices=ApprovalChoices.choices
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def unique_id(self):
        zeros = ["0" for _ in range(6)]
        id_str = str(self.pk)
        for _ in id_str:
            zeros.pop()
        string = ""
        return f"PO{string.join(zeros)}{self.pk}"

    def __str__(self) -> str:
        return self.unique_id

    class Meta:
        ordering = ["-last_modified", "-created_date"]


class PurchaseOrderApproval(models.Model):
    order = models.OneToOneField(
        PurchaseOrder, on_delete=models.CASCADE, related_name="approval_record"
    )
    officer = models.ForeignKey(Staff, on_delete=models.CASCADE)
    approve = models.CharField(max_length=255, choices=ApprovalChoices.choices)
    remarks = models.TextField(max_length=500, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.unique_id
