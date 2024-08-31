from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.procurement.models.rfq_contract import (
    RFQContract,
    RFQNegotiation,
    RFQNegotiationNote,
    NegotiationAndAwardStatusChoices,
)

from apps.core.utilities.errors import get_serializer_error_message
from apps.procurement.api.serializers.rfq_contract import (
    NegotiationNoteCreateSerializer,
)
from apps.vendors.api.serializers.rfq_contract import (
    RFQContractNegotiationSerializer,
)


class RFQNegotiationView(GenericAPIView):
    def post(self, request):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        contract = get_object_or_404(RFQContract, pk=request.data.get("contract_id", 0))

        # TODO: seek my boss for this
        if contract.officer != profile:
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not contract.status == NegotiationAndAwardStatusChoices.PENDING:
            return Response(
                {
                    "message": "Contract is not in processing state. Contract is already %s."
                    % contract.status.capitalize()
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        # TODO: seek my boss for this
        negotiation = get_object_or_404(
            RFQNegotiation, contract=contract, contract__officer=profile
        )

        if not negotiation.status == NegotiationAndAwardStatusChoices.PENDING:
            return Response(
                {
                    "message": "Negotiation is not in processing state. Negotiation is already %s."
                    % negotiation.status.capitalize()
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = NegotiationNoteCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"message": get_serializer_error_message(serializer)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            RFQNegotiationNote.objects.select_for_update().filter().update(
                renegotiated=True
            )
            note: RFQNegotiationNote = serializer.save(author=request.user, contract=contract, renegotiated=False)  # type: ignore
            negotiation.notes.add(note)

            return Response(
                {"message": "Negotiation created successfully.", "id": note.pk},
                status=status.HTTP_201_CREATED,
            )

    def put(self, request):
        return Response(
            {"message": "So far we are not accepting RFQ"},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, contract_id=None):
        """
        Gets all negotiations
        * When contact_id is passed in then it gets negotiations for that particular contract
        """
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        contract = None

        if contract_id:
            contract = get_object_or_404(RFQContract, pk=contract_id)

        self.serializer_class = RFQContractNegotiationSerializer

        if not contract:
            # get all negotiations
            queryset = RFQNegotiation.objects.filter()
            serializer = self.get_serializer(instance=queryset, many=True)
            return Response(
                {"data": serializer.data},
            )

        # get single negotiation based on contract and the vendor
        queryset = get_object_or_404(RFQNegotiation, contract=contract)
        serializer = self.get_serializer(instance=queryset)

        data = {"data": serializer.data}
        return Response(
            data,
        )
