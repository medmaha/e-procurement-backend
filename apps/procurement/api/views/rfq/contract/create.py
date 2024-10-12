#
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from apps.procurement.models.rfq_contract import (
    RFQContract,
    RFQNegotiation,
    NegotiationAndAwardStatusChoices,
    RFQNegotiationNote,
)

from apps.core.utilities.errors import get_serializer_error_message

from apps.procurement.models.rfq import RFQ
from apps.vendors.models.vendor import Vendor
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.generators import generate_unique_id, revert_unique_id
from apps.core.utilities.text_choices import RFQLevelChoices
from apps.procurement.api.serializers.rfq_contract import (
    NegotiationNoteCreateSerializer,
)
from apps.procurement.models.rfq_evaluated import RFQQuotationEvaluation


class CreateContract(CreateAPIView):
    def create(self, request):
        data = request.data
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # TODO validate user authorization
        # Check if the user belongs to a group call RFQ Contract Creator

        # Lock the database
        with transaction.atomic():

            # Get the RFQ in which the contract is/will-be based on
            rfq = (
                RFQ.objects.select_for_update()
                .filter(pk=revert_unique_id("", data.get("rfq_id")))
                .first()
            )
            if not rfq:
                return Response(
                    {"message": "RFQ not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Ensuring that the RFQ is close for quotation submission before issuing any contract
            if rfq.open_status:
                return Response(
                    {
                        "message": "This RFQ is open and needs to be close for processing"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Making sure that the RFQ level is within the bound
            if rfq.level not in [
                RFQLevelChoices.EVALUATION_LEVEL.value,
                RFQLevelChoices.CONTRACT_LEVEL.value,
            ]:
                return Response(
                    {"message": "RFQ level must be at contract/evaluation level"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Get quotation to bind with RFQ for the contract
            rfq_response: RFQResponse = (
                RFQResponse.objects.select_related("rfq", "vendor")
                .select_for_update()
                .filter(rfq=rfq, pk=request.data.get("quotation_id"))
                .first()
            )  # type: ignore

            # Get the evaluation associated with the (RFQ, RFQ_RESPONSE)
            evaluation = RFQQuotationEvaluation.objects.filter(
                quotation=rfq_response, evaluation__rfq=rfq
            ).first()
            if not evaluation:
                return Response(
                    {"message": "RFQ has to evaluated for proceeding to contract"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Checking if contract already exists that matches the quotation and the RFQ
            existing_contract = (
                RFQContract.objects.select_related()
                .filter(rfq_response=rfq_response)
                .exists()
            )
            if existing_contract:
                return Response(
                    {"message": "A contract for this Quotation already exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Checks to see whether the request is made for negotiation purposes or not
            isNegotiation = request.data.get("is_negotiation") is not None

            if not isNegotiation:
                # Get the terms and condition of contract
                terms_and_conditions = request.data.get("terms_and_conditions")
                if not terms_and_conditions or len(str(terms_and_conditions)) < 50:
                    return Response(
                        {
                            "message": "Please specify the terms and conditions of your contract. With a minimum characters of 50"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Attempt to create a new Contract
                contract = RFQContract(
                    rfq=rfq,
                    supplier=rfq_response.vendor,
                    rfq_response=rfq_response,
                    status=NegotiationAndAwardStatusChoices.PENDING,
                    officer=profile,
                    delivery_terms=rfq_response.delivery_terms,
                    validity_period=rfq_response.validity_period,
                    payment_method=rfq_response.payment_method,
                    terms_and_conditions=terms_and_conditions,
                    pricing=int(evaluation.pricing),
                )
                # Create at least one negotiation note
                n = RFQNegotiation()
                n.contract = contract
                n.status = NegotiationAndAwardStatusChoices.PENDING

                note = RFQNegotiationNote()
                note.note = contract.terms_and_conditions
                note.author = contract.officer.user_account
                note.contract = contract
                note.delivery_terms = contract.delivery_terms or ""
                note.payment_method = contract.payment_method or ""
                note.pricing = contract.pricing
                note.save()
                n.save()
                n.notes.add(note)

                try:
                    contract.full_clean()  # Checking all requirements of RFQContract
                    contract.save()
                except Exception as e:
                    return Response(
                        {"message": e},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Congrats so far so good 👍
                return Response(
                    {"message": "Contract created successfully"},
                    status=status.HTTP_201_CREATED,
                )

            contract = RFQContract.objects.create(
                rfq=rfq,
                supplier=rfq_response.vendor,
                rfq_response=rfq_response,
                status=NegotiationAndAwardStatusChoices.PENDING,
                officer=profile,
                pricing=int(rfq_response.pricing),
            )

            note_serializer = NegotiationNoteCreateSerializer(data=data)

            if not note_serializer.is_valid():
                return Response(
                    {"message": get_serializer_error_message(note_serializer)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            negotiation = RFQNegotiation.objects.create(
                contract=contract,
            )
            negotiation_note = note_serializer.save(
                author=request.user, contract=contract
            )
            negotiation.notes.add(negotiation_note)
            return Response(
                {
                    "id": str(generate_unique_id("", contract.pk)),
                    "message": "Successfully created",
                },
                status=status.HTTP_201_CREATED,
            )
