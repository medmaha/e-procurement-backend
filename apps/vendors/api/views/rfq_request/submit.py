import re
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from apps.procurement.models.rfq import RFQ

from apps.vendors.models.rfq_response import (
    RFQResponseBrochure,
    RFQResponse,
)
from apps.core.utilities.text_choices import ApprovalChoices
from apps.core.utilities.errors import get_serializer_error_message


class RFQRespondSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponse
        fields = ["proforma", "form101", "remarks"]


class RFQResponseBrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponseBrochure
        fields = ["name", "file"]


class RFQSubmitView(CreateAPIView):
    serializer_class = RFQRespondSerializer

    def get_brochures(self, request):
        data: dict = request.data
        brochures = []

        def recursive(start: int, end: int):
            for i in range(start, end):
                index = i + 1
                name = f"{index}-brochure-name"
                file = f"{index}-brochure-file"
                if name in data and file in data:
                    brochures.append({"name": data[name], "file": data[file]})

            test = f"{end}-brochure-name"
            if test in data:
                recursive(start + 10, end + 10)

        recursive(0, 10)

        return brochures

    def create(self, request, *args, **kwargs):
        rfq_id = request.data.get("rfq_id")
        rfq = get_object_or_404(RFQ, pk=rfq_id)
        profile_type, profile = request.user.get_profile()

        if profile_type != "Vendor" or profile not in rfq.suppliers.all():
            return Response(
                {"message": "You don't have permissions for this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "reject" in request.data:
            q_response = RFQResponse.objects.create(
                status=ApprovalChoices.REJECTED.value,
                quotation=rfq,
                remarks=request.data.get("remarks", ""),
            )
            rfq.save()
            return Response(
                {"message": "You've successfully rejected the RFQ"},
                status=status.HTTP_201_CREATED,
            )

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            return Response(
                {"message": get_serializer_error_message(serializer)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        brochures = self.get_brochures(request)
        brochures_serializer = RFQResponseBrochureSerializer(
            data=brochures, many=True, context={"request": request}
        )
        if not brochures_serializer.is_valid():
            err_message = get_serializer_error_message(brochures_serializer)
            return Response(
                {"message": err_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            rfq_response: RFQResponse = serializer.save(status=ApprovalChoices.ACCEPTED.value, quotation=rfq)  # type: ignore
            rfq.save()
            b = brochures_serializer.save(rfq_response=rfq_response)
            rfq_response.brochures.set(b)
            return Response(
                {"message": "You quotation was successfully submitted."},
                status=status.HTTP_201_CREATED,
            )
