from rest_framework import serializers
from apps.procurement.models import RFQ, RFQItem, Requisition
from apps.vendors.models.vendor import Vendor
from apps.core.utilities.text_choices import ApprovalChoices


class RFQItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "quantity",
            "item_description",
            "measurement_unit",
            "eval_criteria",
        ]


class RFQCreateSerializer(serializers.ModelSerializer):
    terms_and_conditions = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    description = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = RFQ
        fields = [
            "title",
            "requisition",
            "description",
            "quotation_deadline_date",
            "auto_publish",
            "description",
            "terms_and_conditions",
        ]


# ====================================== List ======================================= #


class RFQItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "id",
            "item_description",
            "quantity",
            "measurement_unit",
            "eval_criteria",
        ]


class RFQRequisitionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = [
            # "title",
            "id",
            "created_date",
        ]


class RFQSupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            # "title",
            "id",
            "name",
        ]


class RFQListSerializer(serializers.ModelSerializer):
    items = RFQItemsListSerializer(many=True)
    suppliers = RFQSupplierListSerializer(many=True)
    requisition = RFQRequisitionListSerializer()

    class Meta:
        model = RFQ
        fields = [
            "id",
            "title",
            "description",
            "terms_and_conditions",
            "items",
            "published",
            "published_at",
            "officer",
            "requisition",
            "level",
            "open_status",
            # "pr_status",
            "approval_status",
            "opened_by",
            "suppliers",
            "created_date",
            "last_modified",
            "quotation_deadline_date",
        ]

    def to_representation(self, instance: RFQ):
        data = super().to_representation(instance)
        if instance.officer:
            data["officer"] = {
                "id": instance.officer.pk,
                "name": instance.officer.name,
                "job_title": instance.officer.job_title,
            }
        return data


class RFQSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQ

        fields = [
            "id",
            "title",
            "created_date",
            "quotation_deadline_date",
        ]
