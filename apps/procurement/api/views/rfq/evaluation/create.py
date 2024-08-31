from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from apps.procurement.models.rfq_evaluated import RFQEvaluation, RFQQuotationEvaluation
from apps.procurement.models.rfq import RFQItem
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.errors import get_serializer_error_message
from apps.procurement.api.serializers.rfq_evaluation import (
    RFQQuotationEvaluationSerializer,
)


class RFQEvaluationCreateView(CreateAPIView):
    serializer_class = RFQQuotationEvaluationSerializer

    def create(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()

        # TODO Validate user authorization

        quotation = get_object_or_404(
            RFQResponse, pk=request.data.get("quotation_id", 0)
        )
        item = get_object_or_404(RFQItem, pk=request.data.get("item_id", 0))

        existing = RFQQuotationEvaluation.objects.filter(item=item, quotation=quotation)
        if existing.exists():
            return Response(
                {"message": "This quotation has already been evaluated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        with transaction.atomic():
            tup = RFQEvaluation.objects.select_for_update().get_or_create(
                rfq=quotation.rfq,
            )
            evaluation, created = tup
            if created:
                evaluation.officer = profile
                evaluation.save()
            data = request.data
            data.update(
                {
                    "quotation": quotation.pk,
                    "officer": profile.pk,
                    "item": item.pk,
                    "status": "submitted",
                }
            )
            serializer = self.get_serializer(data=data, context={"request": request})

            if not serializer.is_valid():
                err_message = get_serializer_error_message(serializer)
                return Response(
                    {"message": err_message}, status=status.HTTP_400_BAD_REQUEST
                )
            quote_evaluation = serializer.save()

            evaluation.evaluations.add(quote_evaluation)

            return Response(
                {"message": "Successful", "id": quote_evaluation.pk},
                status=status.HTTP_201_CREATED,
            )
