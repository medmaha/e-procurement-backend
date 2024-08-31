from  django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.procurement.models.rfq_contract import (
    NegotiationAndAwardStatusChoices,
    RFQContract,
    RFQContractAward,
    RFQNegotiation,
    RFQNegotiationNote,
)
from apps.vendors.api.serializers.rfq_contract import (
    RFQContractListSerializer,
    RFQContractNegotiationSerializer,
)
from apps.procurement.api.serializers.rfq_contract import (
    NegotiationNoteCreateSerializer,
)
from apps.core.utilities.errors import get_serializer_error_message
from apps.core.utilities.generators import generate_unique_id
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.text_choices import RFQLevelChoices
from apps.procurement.models.rfq import RFQ


class RFQContractNegotiationView(GenericAPIView):
    serializer_class = RFQContractListSerializer

    def get_queryset(self, profile):
        queryset = RFQContract.objects.filter(supplier=profile)
        return queryset

    def post(self, request):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Vendor":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        contract = get_object_or_404(RFQContract, pk=request.data.get("contract_id", 0))
        if contract.supplier != profile:
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

        negotiation = get_object_or_404(
            RFQNegotiation, contract=contract, contract__supplier=profile
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
            note: RFQNegotiationNote = serializer.save(author=request.user, contract=contract)  # type: ignore
            negotiation.notes.add(note)

            return Response(
                {"message": "Negotiation created successfully.", "id": note.pk},
                status=status.HTTP_201_CREATED,
            )

    def put(self, request):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Vendor":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        contract = get_object_or_404(RFQContract, pk=request.data.get("contract_id", 0))

        if contract.supplier != profile:
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

        negotiation = get_object_or_404(
            RFQNegotiation, contract=contract, contract__supplier=profile
        )

        if not negotiation.status == NegotiationAndAwardStatusChoices.PENDING:
            return Response(
                {
                    "message": "Negotiation is not in processing state. Negotiation is already %s."
                    % negotiation.status.capitalize()
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        _note = (
            RFQNegotiationNote.objects.select_for_update()
            .filter(
                pk=request.data.get("note_id", 0),
                contract=contract,
                renegotiated=False,
                accepted=False,
            )
            .exclude(author=request.user)
            .first()
        )

        if not _note:
            return Response(
                {
                    "message": "A this negotiation note does not exist or has already been accepted or rejected."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        with transaction.atomic():
            if "accept" in request.data:
                _note.accepted = True
                _note.save()
                # 
                timestamp = timezone.now()
                negotiation.status = NegotiationAndAwardStatusChoices.SUCCESSFUL
                negotiation.outcome  = f"{request.user.full_name} generously accepted the offer. Negotiation ID: {generate_unique_id("N", _note.pk)} awarded to {contract.supplier.name}. on {timestamp.day}-{timestamp.month}-{timestamp.year} at {timestamp.hour}:{timestamp.minute}."
                negotiation.save()
                # 
                contract.status = NegotiationAndAwardStatusChoices.SUCCESSFUL
                contract.pricing = _note.pricing
                contract.validity_period = _note.validity_period
                contract.payment_method = _note.payment_method
                contract.delivery_terms = _note.delivery_terms
                contract.terms_and_conditions = _note.note
                contract.save()
                # 
                award = RFQContractAward()
                award.contract = contract
                award.officer = _note.author.profile
                award.remarks = ""
                award.vendor = profile
                award.status = NegotiationAndAwardStatusChoices.AWARDED
                award.save()
                
                RFQ.objects.select_for_update().filter(pk=contract.rfq.pk).update(level = RFQLevelChoices.INVOICE_LEVEL.value, open_status=False)
                RFQResponse.objects.select_for_update().filter(rfq=contract.rfq).exclude(pk=contract.rfq_response.pk).update(approved_status="rejected", approved_officer = _note.author.profile, approved_date = timezone.now())
                
                RFQResponse.objects.select_for_update().filter(pk=contract.rfq_response.pk).update(
                    approved_status = "accepted",
                    approved_date = timezone.now(),
                    # approved_remarks = _note.note,
                    approved_officer = _note.author.profile,
                )

                return Response(
                    {"message": "Negotiation created successfully.", "id": _note.pk},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"message": "Invalid form data"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def get(self, request, contract_id=None):
        profile_type, profile = request.user.get_profile()

        if profile_type != "Vendor":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        contract = None

        # check if contract exists
        if contract_id:
            contract = get_object_or_404(RFQContract, pk=contract_id)

        self.serializer_class = RFQContractNegotiationSerializer
        if not contract:
            # get all negotiations for this vendor
            queryset = RFQNegotiation.objects.filter(contract__supplier=profile)
            serializer = self.get_serializer(instance=queryset, many=True)
            return Response(
                {"data": serializer.data},
            )

        # get single negotiation based on contract and the vendor
        queryset = get_object_or_404(
            RFQNegotiation, contract__supplier=profile, contract=contract
        )
        serializer = self.get_serializer(instance=queryset)

        data = {"data": serializer.data}
        return Response(
            data,
        )
