from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.vendors.api.serializers.rfq_requests import RFQRequestListSerializer


class RFQRequestListView(ListAPIView):
    serializer_class = RFQRequestListSerializer

    def get_queryset(self, vendor):
        queryset = vendor.rfq_requests.filter()
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
