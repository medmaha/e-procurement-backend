from rest_framework import serializers
from apps.procurement.models import RFQ, RFQItem, Requisition
from apps.vendors.models.vendor import Vendor
from apps.core.utilities.text_choices import ApprovalChoices


class RFQItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "item_description",
            "quantity",
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
            "items",
            "requisition",
            "title",
            "description",
            "required_date",
            "auto_publish",
            "description",
            "terms_and_conditions",
        ]


# ====================================== List ======================================= #


class RFQItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
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
            "unique_id",
            "id",
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
            "officer",
            "requisition",
            "unique_id",
            "deadline",
            "level",
            "open_status",
            "approval_status",
            "opened_by",
            "suppliers",
            "created_date",
            "last_modified",
        ]

    def to_representation(self, instance: RFQ):
        data = super().to_representation(instance)
        if instance.officer:
            data["officer"] = {
                "id": instance.officer.pk,
                "name": instance.officer.name,
                "employee_id": instance.officer.employee_id,
            }
        if instance.requires_gppa_approval:
            try:
                approval_record = instance.approval_record  # type: ignore
                if approval_record and not approval_record.gppa_approval:
                    data["approval_status"] = ApprovalChoices.PENDING
            except:
                pass
        if data["approval_status"].lower() == "accepted" and not instance.published:
            data["publishable"] = True
        data["editable"] = False
        if "request" in self.context:
            request = self.context["request"]
            profile_type, profile = request.user.get_profile()

            if profile_type == "Staff":
                if request.user.has_perm("procurement.add_rfqapproval"):
                    if data["approval_status"].lower() == ApprovalChoices.PENDING:
                        data["approvable"] = True
                        try:
                            if instance.approval_record:  # type: ignore
                                data["approvable"] = False
                        except:
                            pass
            if profile_type == "GPPA":
                if request.user.has_perm("procurement.add_rfqapprovalgppa"):
                    if data["approval_status"].lower() == ApprovalChoices.PENDING:
                        data["approvable"] = True
                        try:
                            if instance.approval_record_gppa:  # type: ignore
                                data["approvable"] = False
                        except:
                            pass
        data["status"] = data["approval_status"]

        # Because perhaps the officer would like to make an update to the RFQ
        if data.get("approvable"):
            data["auto_publish"] = instance.auto_publish
            data["terms_and_conditions"] = instance.terms_and_conditions
        return data


class RFQSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQ

        fields = [
            "title",
            "unique_id",
            "id",
            "editable",
        ]
