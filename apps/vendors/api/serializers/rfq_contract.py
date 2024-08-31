from rest_framework import serializers
from apps.procurement.models.rfq_contract import (
    NegotiationAndAwardStatusChoices,
    RFQContract,
    RFQContractAward,
    RFQNegotiation,
    RFQNegotiationNote,
)


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
            "payment_method",
            "validity_period",
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

        data["negotiations"] = instance.negotiation.filter().count()  # type: ignore
        return data


class RFQContractNotificationNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQNegotiationNote
        fields = [
            "id",
            "note",
            "file",
            "pricing",
            "delivery_terms",
            "payment_method",
            "validity_period",
            "renegotiated",
            "accepted",
            "created_date",
        ]

    def to_representation(self, instance: RFQNegotiationNote):
        data = super().to_representation(instance)
        author = instance.author
        data["author"] = {
            "id": author.pk,
            "name": author.full_name,
            "profile_type": author.profile_type,
        }
        return data


class RFQContractNegotiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQNegotiation
        fields = [
            "id",
            "status",
            "outcome",
            "created_date",
            "last_modified",
        ]

    def to_representation(self, instance: RFQNegotiation):
        data = super().to_representation(instance)
        data["contract"] = {
            "id": instance.contract.pk,
            "name": str(instance.contract.rfq.unique_id),
        }
        data["supplier"] = {
            "id": instance.contract.supplier.pk,
            "name": instance.contract.supplier.name,
        }

        data["can_award"] = (
            instance.status == NegotiationAndAwardStatusChoices.SUCCESSFUL.value
            and not RFQContractAward.objects.filter(contract=instance.contract)
        )

        data["rfq"] = {
            "id": instance.contract.rfq.pk,
            "unique_id": instance.contract.rfq.unique_id,
        }
        data["officer"] = {
            "id": instance.contract.officer.pk,
            "name": instance.contract.officer.name,
        }
        data["notes"] = RFQContractNotificationNodeSerializer(
            instance=instance.notes.filter(), many=True
        ).data
        # instance.status = NegotiationAndAwardStatusChoices.ACTIVE
        return data
