from rest_framework import serializers
from apps.procurement.models import PurchaseOrder, PurchaseOrderApproval
from apps.procurement.api.serializers.rfq import RFQListSerializer
from apps.procurement.api.serializers.quotations import (
    RFQResponseRetrieveSerializer,
)


# =========================================== LIST ============================================= #
class PurchaseOrderListSerializer(serializers.ModelSerializer):
    officer = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    rfq = serializers.SerializerMethodField()
    quote = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "unique_id",
            "comments",
            "rfq",
            "quote",
            "vendor",
            "officer",
            "created_date",
            "last_modified",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.status
        if "request" in self.context and instance.status.lower() == "pending":
            user = self.context["request"].user
            if user.has_perm("procurement.add_purchaseorderapproval"):
                data["approvable"] = True
        return data

    def get_rfq(self, obj: PurchaseOrder):
        rfq = obj.rfq
        return {"id": rfq.pk, "unique_id": rfq.unique_id}

    def get_quote(self, obj: PurchaseOrder):
        return {"id": obj.rfq_response.pk, "unique_id": obj.rfq_response.unique_id}

    def get_officer(self, obj: PurchaseOrder):
        return {"id": obj.officer.pk, "name": obj.officer.name}

    def get_vendor(self, obj: PurchaseOrder):
        return {"id": obj.vendor.pk, "name": obj.vendor.name}


# =========================================== Retrieve ============================================= #
class PurchaseOrderRetrieveSerializer(serializers.ModelSerializer):
    officer = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    rfq = RFQListSerializer()
    quotation_response = RFQResponseRetrieveSerializer()

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "unique_id",
            "comments",
            "rfq",
            "quotation_response",
            "vendor",
            "officer",
            "created_date",
            "last_modified",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.status
        if "request" in self.context and instance.status.lower() == "pending":
            user = self.context["request"].user
            if user.has_perm("procurement.add_purchaseorderapproval"):
                data["approvable"] = True

        return data

    def get_officer(self, obj: PurchaseOrder):
        return {"id": obj.officer.pk, "name": obj.officer.name}

    def get_vendor(self, obj: PurchaseOrder):
        return {"id": obj.vendor.pk, "name": obj.vendor.name}
