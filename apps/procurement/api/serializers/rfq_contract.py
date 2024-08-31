from rest_framework import serializers
from apps.procurement.models.rfq_contract import (
    RFQContract,
    RFQContractAward,
    NegotiationAndAwardStatusChoices,
    RFQNegotiation,
    RFQNegotiationNote,
)


class NegotiationNoteCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        allow_empty_file=False, required=False, allow_null=True
    )

    class Meta:
        model = RFQNegotiationNote
        fields = [
            "pricing",
            "delivery_terms",
            "payment_method",
            "validity_period",
            "note",
            "file",
        ]


class RFQContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQContract
        fields = [
            "id",
            "status",
            "created_date",
            "last_modified",
            "delivery_terms",
            "pricing",
            "terms_and_conditions",
            "payment_method",
            "validity_period",
            "deadline_date",
        ]

    def to_representation(self, instance: RFQContract):
        data = super().to_representation(instance)
        data["supplier"] = {
            "id": instance.supplier.pk,
            "name": instance.supplier.name,
        }

        data["rfq"] = {
            "id": instance.rfq.pk,
            "unique_id": instance.rfq.unique_id,
        }
        data["officer"] = {
            "id": instance.officer.pk,
            "name": instance.officer.name,
        }

        return data
