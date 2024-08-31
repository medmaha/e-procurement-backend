from rest_framework import serializers
from apps.procurement.models import RFQ, RFQItem
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.text_choices import ApprovalChoices


class RFQRequestItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "item_description",
            "quantity",
            "measurement_unit",
            "eval_criteria",
        ]


class RFQRequestListSerializer(serializers.ModelSerializer):
    items = RFQRequestItemsListSerializer(many=True)

    class Meta:
        model = RFQ
        fields = [
            "id",
            "unique_id",
            "title",
            "description",
            "items",
            "deadline",
            "open_status",
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
        request = self.context.get("request")
        my_response = None
        vendor = None

        if request:
            profile_type, profile = request.user.get_profile()
            if profile_type == "Vendor":
                vendor = profile
                my_response = RFQResponse.objects.filter(
                    rfq=instance, vendor=profile
                ).first()
                data["responded"] = my_response is not None

        if my_response:
            data["my_response"] = my_response.status.lower()
        else:
            data["my_response"] = ApprovalChoices.PENDING.value.lower()

        if vendor:
            data["vendor"] = {"id": vendor.pk, "name": vendor.organization_name}
        else:
            data["vendor"] = {}

        return data


class RFQRequestSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQ
        fields = [
            "title",
            "unique_id",
            "id",
            "editable",
        ]
