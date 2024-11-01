from rest_framework import serializers
from apps.vendors.models import (
    RFQResponse,
    RFQResponseBrochure,
)
from apps.organization.models.staff import Staff
from apps.procurement.models.rfq import RFQ, RFQItem
from apps.core.utilities.text_choices import ApprovalChoices
from apps.procurement.models.rfq_evaluated import RFQQuotationEvaluation


class RFQOfficerSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ["id", "name", "department"]

    def get_department(self, obj: Staff):
        return obj.unit.department.name


class RFQItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "id",
            "quantity",
            "eval_criteria",
            "item_description",
            "measurement_unit",
        ]


class RFQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQ
        fields = [
            "id",
            "title",
            "quotation_deadline_date",
            "level",
            "open_status",
            "approval_status",
            "created_date",
        ]

    def to_representation(self, instance: RFQ):
        data = super().to_representation(instance)
        if instance.officer:
            data["officer"] = {
                "id": instance.officer.pk,
                "name": instance.officer.name,
                "employee_id": instance.officer.employee_id,
            }
        return data


# ================================================================ Rfq Response Serializers ==================================================#


class RFQRespondSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponse
        fields = ["id", "unique_id"]


class RFQResponseBrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponseBrochure
        fields = ["id", "name", "file"]


class RFQResponseListSerializer(serializers.ModelSerializer):
    rfq = RFQListSerializer()
    deadline = serializers.SerializerMethodField()

    status = serializers.SerializerMethodField()
    approved_status = serializers.SerializerMethodField()

    class Meta:
        model = RFQResponse
        fields = [
            "id",
            "approved_status",
            "created_date",
            "status",
            "rfq",
            "deadline",
            "proforma",
            "form101",
            "remarks",
            "pricing",
            "delivery_date",
            "validity_period",
            "payment_method",
            "last_modified",
            "created_date",
        ]

    def get_deadline(self, obj):
        return obj.rfq.quotation_deadline_date

    def get_status(self, obj):
        return obj.status.upper()

    def get_approved_status(self, obj):
        return obj.approved_status.upper()

    def to_representation(self, instance: RFQResponse):
        data = super().to_representation(instance)
        data["brochures"] = RFQResponseBrochureSerializer(
            instance=instance.brochures.filter(), many=True, context=self.context
        ).data
        data["vendor"] = {
            "id": instance.vendor.pk,
            "name": instance.vendor.name,
        }
        if not self.context.get("slim"):
            evaluations = RFQQuotationEvaluation.objects.select_related(
                "officer"
            ).filter(quotation=instance)
            if evaluations.exists():
                data["evaluation"] = []
                for evaluation in evaluations:
                    data["evaluation"].append(
                        {
                            "item_id": evaluation.item.pk,  # type: ignore
                            "id": evaluation.pk,  # type: ignore
                            "rating": evaluation.rating,
                            "comments": evaluation.comments,
                            "status": evaluation.status,
                            "pricing": evaluation.pricing,
                            "specifications": evaluation.specifications,
                            "quantity": evaluation.quantity,
                            "status": evaluation.status,
                        }
                    )

        return data


class RFQResponseRetrieveSerializer(serializers.ModelSerializer):
    rfq = RFQListSerializer()
    invited_at = serializers.SerializerMethodField()
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
            "pricing",
            "delivery_date",
            "validity_period",
            "payment_method",
            "approved_status",
        ]

    def get_deadline(self, obj):
        return str(obj.rfq.deadline)

    def get_approved_status(self, obj):
        return obj.approved_status.upper()

    def get_invited_at(self, obj):
        return obj.rfq.created_date

    def to_representation(self, instance: RFQResponse):
        data = super().to_representation(instance)
        data["brochures"] = RFQResponseBrochureSerializer(
            instance=instance.brochures.filter(), many=True, context=self.context
        ).data
        data["deadline"] = str(instance.rfq.quotation_deadline_date)
        data["vendor"] = {
            "id": instance.vendor.pk,
            "name": instance.vendor.name,
        }
        return data
