from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.vendors.models.rfq_response import RFQResponse
from apps.vendors.api.serializers.rfq_response import (
    RFQResponseRetrieveSerializer,
)


class RFQRespondGetAPIView(RetrieveAPIView):
    serializer_class = RFQResponseRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        queryset = get_object_or_404(RFQResponse, quotation__pk=kwargs.get("id"))
        serializer = self.get_serializer(self.filter_queryset(queryset))
        return Response({"data": serializer.data})
