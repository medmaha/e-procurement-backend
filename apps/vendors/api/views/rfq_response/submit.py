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


class RFQRespondCreateSerializer(serializers.ModelSerializer):
    form101 = serializers.FileField(
        required=False, allow_empty_file=True, allow_null=True
    )

    class Meta:
        model = RFQResponse
        fields = [
            "proforma",
            "form101",
            "remarks",
            "pricing",
            "delivery_terms",
            "payment_method",
            "validity_period",
        ]


class RFQResponseBrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQResponseBrochure
        fields = ["name", "file"]


class RFQSubmitView(CreateAPIView):
    serializer_class = RFQRespondCreateSerializer

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
            rfq_response = RFQResponse.objects.create(
                status=ApprovalChoices.REJECTED.value,
                rfq=rfq,
                vendor=profile,
                pricing=0,
                delivery_terms="-",
                payment_method="-",
                validity_period="-",
                remarks=request.data.get("remarks", ""),
            )
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

        brochures_data = self.get_brochures(request)
        brochures_serializer = RFQResponseBrochureSerializer(
            data=brochures_data, many=True, context={"request": request}
        )
        if not brochures_serializer.is_valid():
            err_message = get_serializer_error_message(brochures_serializer)
            return Response(
                {"message": err_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            rfq_response: RFQResponse = serializer.save(status=ApprovalChoices.ACCEPTED.value, vendor=profile, rfq=rfq)  # type: ignore
            brochures = brochures_serializer.save(rfq_response=rfq_response)
            rfq_response.brochures.set(brochures)
            return Response(
                {"message": "You quotation was successfully submitted."},
                status=status.HTTP_201_CREATED,
            )
