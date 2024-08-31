from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from apps.vendors.api.serializers.list import Vendor, VendorSelectSerializer


class VendorSelectView(ListAPIView):
    serializer_class = VendorSelectSerializer

    def get_queryset(self):
        qs = Vendor.objects.filter(active=True)
        return qs

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {"data": serializer.data}
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
