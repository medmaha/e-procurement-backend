import threading
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.vendors.models.rfq_response import RFQResponse
from apps.vendors.api.serializers.rfq_response import RFQResponseListSerializer


class RFQResponseListView(ListAPIView):
    serializer_class = RFQResponseListSerializer

    def get_queryset(self, vendor):
        queryset = RFQResponse.objects.filter(vendor=vendor, status="accepted")
        return queryset

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        if profile_type != "Vendor":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )
        queryset = self.get_queryset(vendor)
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        return Response({"data": serializer.data})
