from rest_framework import serializers
from apps.procurement.models.rfq_evaluated import (
    RFQEvaluation,
    RFQEvaluationApprover,
    RFQQuotationEvaluation,
)
from apps.procurement.api.serializers.quotations import RFQItemsSerializer

# ===============================================================  CREATE =========================================================== #


class RFQEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQEvaluation
        exclude = ["id", "evaluations"]

    def to_representation(self, instance: RFQEvaluation):
        data = super().to_representation(instance)
        data["id"] = instance.pk
        data["rfq"] = {"id": instance.rfq.pk}
        # data["requirements"] = RFQItemsSerializer(instance.rfq.items, many=True).data
        data["officer"] = {
            "id": instance.officer.pk,  # type:ignore
            "name": instance.officer.name,  # type:ignore
        }
        return data


class RFQQuotationEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQQuotationEvaluation
        exclude = ["id"]

    def to_representation(self, instance: RFQQuotationEvaluation):
        data = super().to_representation(instance)
        data["id"] = instance.pk  # type:ignore
        data["officer"] = {
            "id": instance.officer.pk,  # type:ignore
            "name": instance.officer.name,  # type:ignore
        }
        if not self.context.get("slim"):
            data["item"] = {
                "id": instance.item.pk,
                "name": instance.item.item_description,
            }
            data["quotation"] = {
                "id": instance.quotation.pk,  # type:ignore
                "submitted_date": str(instance.created_date),  # type:ignore
                "vendor": {
                    "id": instance.quotation.vendor.pk,
                    "name": instance.quotation.vendor.name,
                },
            }
        else:
            pass
            # data["quotation"] = {
            #     "id": instance.quotation.pk,  # type:ignore
            #     "submitted_date": str(instance.created_date),  # type:ignore
            # }

        return data


class RFQQuotationWinnerEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQQuotationEvaluation
        fields = ["id", "quantity", "rating", "pricing", "specifications", "comments"]

    def to_representation(self, instance: RFQQuotationEvaluation):
        data = super().to_representation(instance)
        data["id"] = instance.pk  # type:ignore
        data["officer"] = {
            "id": instance.officer.pk,  # type:ignore
            "name": instance.officer.name,  # type:ignore
        }
        if not self.context.get("slim"):
            data["item"] = {
                "id": instance.item.pk,
                "name": instance.item.item_description,
            }
            data["quotation"] = {
                "id": instance.quotation.pk,  # type:ignore
                "submitted_date": str(instance.created_date),  # type:ignore
                "vendor": {
                    "id": instance.quotation.vendor.pk,
                    "name": instance.quotation.vendor.name,
                },
            }

        return data


class RFQEvaluationApproverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQEvaluationApprover
        fields = "__all__"
