from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from apps.procurement.models.rfq_evaluated import RFQEvaluation
from apps.procurement.api.serializers.rfq_evaluation import (
    RFQEvaluationSerializer,
    RFQQuotationEvaluationSerializer,
)
from apps.procurement.models.rfq import RFQ
from apps.core.utilities.generators import revert_unique_id


class RFQEvaluationRetrieveView(RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()
        if profile_type != "Staff":
            return Response(
                {"message": "Permission denied! Only staff can retrieve evaluation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # TODO - Check if profile has permission to to view this evaluation

        rfq_id = revert_unique_id(None, kwargs.get("rfq_id", 0))
        rfq = get_object_or_404(RFQ, pk=rfq_id)
        evaluation = get_object_or_404(RFQEvaluation, rfq=rfq)
        if evaluation.officer != profile:
            return Response(
                {
                    "message": "Permission denied! Only evaluation officer can remove evaluation."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        evaluations = evaluation.evaluations.all()
        serializer = RFQQuotationEvaluationSerializer(evaluations, many=True)
        winners = evaluation.determine_winner(evaluations)

        return Response(
            {
                "data": serializer.data,
                "extras": {
                    "evaluation": RFQEvaluationSerializer(instance=evaluation).data,
                    "winners": winners,
                },
            },
            status=status.HTTP_200_OK,
        )
