from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.procurement.models.rfq_contract import RFQContract, RFQNegotiation
from apps.vendors.api.serializers.rfq_contract import RFQContractListSerializer


class RFQContractListView(GenericAPIView):
    def get(self, request, contract_id=None):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        contract = None
        if contract_id:
            contract = get_object_or_404(
                RFQContract, pk=contract_id
            )

        self.serializer_class = RFQContractListSerializer
        if not contract:
            # get all contracts
            queryset = RFQContract.objects.filter()
            serializer = self.get_serializer(instance=queryset, many=True)
            return Response(
                {"data": serializer.data},
            )

        # get single negotiation based on contract and the vendor
        queryset = get_object_or_404(
            RFQContract, negotiation__contract__pk=contract.pk
        )
        serializer = self.get_serializer(instance=queryset)

        data = {"data": serializer.data}
        return Response(
            data,
        )
