from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from apps.procurement.models.rfq_contract import RFQContract
from apps.vendors.api.serializers.rfq_contract import RFQContractListSerializer


class RFQContractListView(ListAPIView):
    serializer_class = RFQContractListSerializer

    def get_queryset(self, profile):
        queryset = RFQContract.objects.filter(supplier=profile)
        return queryset

    def list(self, request):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Vendor":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )
        queryset = self.filter_queryset(self.get_queryset(profile))
        serializer = self.get_serializer(queryset, many=True)

        data = {"data": serializer.data}
        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )
