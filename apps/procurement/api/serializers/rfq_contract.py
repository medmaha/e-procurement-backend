from rest_framework import serializers
from apps.procurement.models.rfq_contract import (
    RFQContract,
    RFQNegotiationNote,
    RFQContractApproval,
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


class ContractApprovalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQContractApproval
        fields = [
            "approve",
            "remarks",
            "officer",
            "contract",
        ]


class ContractApprovalRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQContractApproval
        fields = [
            "id",
            "approve",
            "remarks",
            "date_created",
            "last_modified",
        ]

    def to_representation(self, instance: RFQContractApproval):
        data = super().to_representation(instance)
        data["officer"] = {
            "id": instance.officer.pk,
            "name": instance.officer.name,
        }
        data["contract"] = {
            "id": instance.contract.pk,
            "pricing": instance.contract.pricing,
            "duration": instance.contract.deadline_date,
        }
        return data


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
