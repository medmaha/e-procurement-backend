from rest_framework import serializers
from apps.vendors.models import (
    RFQResponseBrochure,
)
from apps.procurement.api.serializers.rfq import RFQListSerializer
from apps.vendors.models.rfq_response import RFQResponse


class RFQRespondSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponse
        fields = ["id", "unique_id"]


class RFQResponseListSerializer(serializers.ModelSerializer):
    rfq = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    approved_status = serializers.SerializerMethodField()

    class Meta:
        model = RFQResponse
        fields = [
            "id",
            "unique_id",
            "status",
            "approved_status",
            "created_date",
            "rfq",
            "deadline",
            "proforma",
            "form101",
            "remarks",
            "pricing",
            "delivery_date",
            "payment_method",
            "validity_period",
            "last_modified",
            "created_date",
        ]

    def get_deadline(self, obj: RFQResponse):
        return obj.rfq.quotation_deadline_date

    def get_status(self, obj):
        return obj.status.upper()

    def get_approved_status(self, obj):
        return obj.approved_status.upper()

    def get_rfq(self, obj):
        return {
            "id": obj.rfq.pk,
            "items": obj.rfq.items.filter().values(
                "id",
                "item_description",
                "quantity",
                "measurement_unit",
                "eval_criteria",
                "remark",
            ),
            "published_at": obj.rfq.published_at,
        }

    def to_representation(self, instance: RFQResponse):
        data = super().to_representation(instance)
        data["brochures"] = RFQResponseBrochureListSerializer(
            instance=instance.brochures.filter(), many=True, context=self.context
        ).data
        data["vendor"] = {
            "id": instance.vendor.pk,
            "name": instance.vendor.organization_name,
            "alias": instance.vendor.alias,
        }
        return data


class RFQResponseRetrieveSerializer(serializers.ModelSerializer):
    rfq = RFQListSerializer()
    invited_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    approved_status = serializers.SerializerMethodField()

    class Meta:
        model = RFQResponse
        fields = [
            "id",
            "status",
            "proforma",
            "form101",
            "rfq",
            "created_date",
            "last_modified",
            "unique_id",
            "invited_at",
            "remarks",
            "approved_status",
        ]

    def get_deadline(self, obj):
        return str(obj.rfq.deadline)

    def get_status(self, obj):
        return obj.status.upper()

    def get_approved_status(self, obj):
        return obj.approved_status.upper()

    def get_invited_at(self, obj):
        return obj.rfq.created_date

    def to_representation(self, instance: RFQResponse):
        data = super().to_representation(instance)
        data["brochures"] = RFQResponseBrochureListSerializer(
            instance=instance.brochures.filter(), many=True, context=self.context
        ).data
        data["deadline"] = str(instance.rfq.deadline)
        data["vendor"] = {
            "id": instance.vendor.pk,
            "name": instance.vendor.organization_name,
        }
        return data


# ================================================ BROCHURES LIST ============================================== #


class RFQResponseBrochureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponseBrochure
        fields = ["id", "name", "file", "created_date"]


class RFQResponseBrochureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponseBrochure
        fields = ["name", "file"]
