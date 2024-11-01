from django.db import connection
from django.db.models import Q, OuterRef, Subquery, F, Case, When, Prefetch
from django.db.models.manager import BaseManager
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.core.utilities.text_choices import ApprovalChoices
from apps.vendors.api.serializers.rfq_requests import (
    RFQ,
    RFQRequestListSerializer,
)


class RFQRequestListView(ListAPIView):
    serializer_class = RFQRequestListSerializer

    def get_queryset(self, vendor):

        rfq_requests: BaseManager[RFQ] = vendor.rfq_requests

        # Subquery to get the most recent response ID and status for the vendor.
        vendor_response_id = (
            rfq_requests.only("responses__id")
            .filter(responses__vendor_id=vendor.pk, id=OuterRef("pk"))
            .values("responses__id")[:1]
        )

        vendor_response_status = (
            rfq_requests.only("responses__status")
            .filter(responses__vendor_id=vendor.pk, id=OuterRef("pk"))
            .values("responses__status")[:1]
        )

        queryset = (
            rfq_requests.select_related("officer")
            .prefetch_related("items")
            .annotate(
                my_response=Subquery(vendor_response_status),
                my_response_id=Subquery(vendor_response_id),
            )
            .filter(approval_status=ApprovalChoices.APPROVED)
        )
        return queryset

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        if profile_type != "Vendor":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = self.get_queryset(vendor)
        serializer = self.get_serializer(
            self.filter_queryset(queryset), many=True, context={"request": request}
        )

        return Response({"data": serializer.data})
