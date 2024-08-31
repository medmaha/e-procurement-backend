from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.procurement.api.serializers.quotations import (
    RFQResponseListSerializer,
    RFQRespondSelectSerializer,
)
from backend.apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.text_choices import ApprovalChoices


class QuotationRespondListView(ListAPIView):
    serializer_class = RFQResponseListSerializer

    def get_queryset(self):
        queryset = RFQResponse.objects.filter(
            # quotation__rfq_id=self.kwargs["rfq_id"]
            # status="accepted",
        )
        return queryset

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        queryset = self.get_queryset()
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)

        auth_perms = {
            "update": request.user.has_perm("vendors.change_quotationresponse"),
        }

        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
            status=status.HTTP_200_OK,
        )


class QuotationRespondSelectView(ListAPIView):
    serializer_class = RFQRespondSelectSerializer

    def get_queryset(self, profile_type):
        if profile_type == "Vendor":
            "Selecting Quotes for invoicing"
            return RFQResponse.objects.filter(
                status=ApprovalChoices.ACCEPTED.value, evaluation_status="accepted"
            )

        "Selecting Quotes for evaluation or purchase orders"
        return RFQResponse.objects.filter(
            status=ApprovalChoices.ACCEPTED.value, evaluation_status="processing"
        )

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        queryset = self.get_queryset(profile_type)
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )
