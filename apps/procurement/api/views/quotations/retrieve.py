from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.procurement.api.serializers.quotations import (
    RFQResponseListSerializer,
)
from backend.apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.generators import revert_generated_unique_id


class QuotationRespondRetrieveView(RetrieveAPIView):
    serializer_class = RFQResponseListSerializer

    def retrieve(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        slug = revert_generated_unique_id(None, self.kwargs.get("id") or "0")
        queryset = get_object_or_404(RFQResponse, pk=slug)
        serializer = self.get_serializer(queryset)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
