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
        data["officer"] = (
            {
                "id": instance.officer.pk,
                "name": instance.officer.name,
                "job_title": instance.officer.job_title,
            }
            if instance.officer
            else None
        )
        if not self.context.get("slim"):
            data["item"] = {
                "id": instance.item.pk,
                "name": instance.item.item_description,
            }
            data["quotation"] = {
                "id": instance.quotation.pk,
                "pricing": instance.quotation.pricing,
                "submitted_date": str(instance.created_date),
                "delivery_date": str(instance.quotation.delivery_date),
                "evaluation_status": instance.quotation.evaluation_status,
                "vendor": {
                    "id": instance.quotation.vendor.pk,
                    "logo": instance.quotation.vendor.logo,
                    "name": instance.quotation.vendor.name,
                    "short_desc": instance.quotation.vendor.short_desc,
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
            "job_title": instance.officer.job_title,  # type:ignore
        }
        data["item"] = {
            "id": instance.item.pk,
            "name": instance.item.item_description,
        }
        data["quotation"] = {
            "id": instance.quotation.pk,
            "pricing": instance.quotation.pricing,
            "submitted_date": str(instance.created_date),
            "delivery_date": str(instance.quotation.delivery_date),
            "evaluation_status": instance.quotation.evaluation_status,
            "vendor": {
                "id": instance.quotation.vendor.pk,
                "logo": instance.quotation.vendor.logo,
                "name": instance.quotation.vendor.name,
                "short_desc": instance.quotation.vendor.short_desc,
            },
        }

        return data


class RFQEvaluationApproverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQEvaluationApprover
        fields = "__all__"
