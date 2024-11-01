from rest_framework import serializers
from apps.procurement.models import RFQ, RFQItem
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.text_choices import ApprovalChoices


class RFQRequestItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = [
            "id",
            "item_description",
            "quantity",
            "measurement_unit",
            "eval_criteria",
        ]


class RFQRequestListSerializer(serializers.ModelSerializer):
    items = RFQRequestItemsListSerializer(many=True)

    my_response = serializers.ChoiceField(
        choices=ApprovalChoices.choices, default=ApprovalChoices.PENDING
    )
    my_response_id = serializers.IntegerField()

    class Meta:
        model = RFQ
        fields = [
            "id",
            "title",
            "description",
            "items",
            "my_response",
            "my_response_id",
            "quotation_deadline_date",
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
                "job_title": instance.officer.job_title,
            }

        data["my_response"] = data.get("my_response", ApprovalChoices.PENDING.value)

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
