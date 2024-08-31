from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from backend.apps.vendors.models.rfq_response import RFQResponse


class QuotationRespondRejectView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        profile_type, staff = request.user.get_profile()

        if profile_type != "Staff" or not request.user.has_perm(
            "vendors.change_quotationresponse"
        ):
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        quote = get_object_or_404(RFQResponse, pk=request.data.get("quote_id"))
        print(quote.evaluation_status)
        if quote.evaluation_status != "processing":
            return Response(
                {"message": "This quote has already been evaluated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Reject the quotation
        RFQResponse.objects.filter(pk=quote.pk).update(
            evaluation_officer=staff,
            evaluation_status="rejected",
            evaluation_remarks=request.data.get("remarks", ""),
        )

        return Response(
            {"message": "Quotation rejected successfully"}, status=status.HTTP_200_OK
        )
