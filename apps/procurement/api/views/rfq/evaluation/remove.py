from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import DestroyAPIView
from apps.procurement.models.rfq_evaluated import RFQEvaluation, RFQQuotationEvaluation
from apps.procurement.models.rfq import RFQItem
from apps.vendors.models.rfq_response import RFQResponse


class RFQEvaluationRemoveView(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            return Response(
                {"message": "Permission denied! You're forbidden for this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        with transaction.atomic():
            quotation = get_object_or_404(
                RFQResponse, pk=request.data.get("quotation_id", 0)
            )
            item = get_object_or_404(RFQItem, pk=request.data.get("item_id", 0))
            quote_evaluation = get_object_or_404(
                RFQQuotationEvaluation, pk=request.data.get("eval_id", 0)
            )
            if quote_evaluation.quotation != quotation or quote_evaluation.item != item:
                return Response(
                    {"message": "Error! Invalid Quotation for evaluation."},
                )

            if quote_evaluation.officer != profile:
                return Response(
                    {
                        "message": "Permission denied! Only evaluation officer can remove evaluation."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            evaluation = (
                RFQEvaluation.objects.select_for_update()
                .filter(rfq=quotation.rfq)
                .first()
            )
            if not evaluation:
                return Response(
                    {"message": "Error! Invalid Quotation for evaluation."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if quote_evaluation in evaluation.evaluations.select_related().filter():
                evaluation.evaluations.remove(quote_evaluation)
                quote_evaluation.delete()
                return Response(
                    {"message": "Evaluation removed successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                {"message": "Error! Invalid Quotation for evaluation."},
                status=status.HTTP_400_BAD_REQUEST,
            )
