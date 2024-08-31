from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.procurement.models import RFQ, PurchaseOrder
from apps.vendors.models import Vendor, RFQResponse


class PurchaseOrderCreateView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        profile_type, staff = request.user.get_profile()

        # if profile_type != "Staff" or not request.user.has_perm(
        #     "procurement.add_purchaseorder"
        # ):
        #     return Response(
        #         {"message": "You don't have permission to perform this action"},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        quote_id = request.data.get("quote_id")
        quote = get_object_or_404(RFQResponse, pk=quote_id)

        if quote.evaluation_status != "processing":
            return Response(
                {"message": "This quote has already been evaluated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        rfq = quote.quotation.rfq
        vendor = quote.quotation.vendor
        comments = request.data.get("comments", "")
        auto_publish = request.data.get("auto_publish") == "on"
        requires_approval = request.data.get("requires_approval") == "on"

        PurchaseOrder.objects.create(
            rfq=rfq,
            quote=quote,
            officer=staff,
            vendor=vendor,
            comments=comments,
            auto_publish=auto_publish,
            requires_approval=requires_approval,
        )

        # Update the evaluation status of the quote
        RFQResponse.objects.filter(pk=quote.pk).update(
            evaluation_officer=staff,
            evaluation_remarks=comments,
            evaluation_status="accepted",
        )

        return Response(
            {"message": "Purchase order created successfully"},
            status=status.HTTP_201_CREATED,
        )
