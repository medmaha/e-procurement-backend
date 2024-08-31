from rest_framework import serializers
from apps.vendors.models import Invoice
from apps.procurement.api.serializers.purchase_order import (
    PurchaseOrderListSerializer,
)


class InvoiceListSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    purchase_order = PurchaseOrderListSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        exclude = []

    def get_vendor(self, instance: Invoice):
        return {
            "id": instance.vendor.pk,  # type: ignore
            # "unique_id":instance.vendor.pk,
            "name": instance.vendor.name,  # type: ignore
        }
