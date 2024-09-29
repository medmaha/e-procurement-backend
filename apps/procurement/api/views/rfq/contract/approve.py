from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.accounts.models import Account
from apps.procurement.models.rfq_contract import (
    RFQContract,
    RFQContractApproval,
    ApprovalChoices,
)
from apps.procurement.api.serializers.rfq_contract import (
    ContractApprovalCreateSerializer,
    ContractApprovalRetrieveSerializer,
)
from apps.core.utilities.errors import get_serializer_error_message


class ContractApprovalCreateAPIView(CreateAPIView):
    """API handler for contract approval creation"""

    serializer_class = ContractApprovalCreateSerializer

    def create(self, request, contract_id):
        user: Account = request.user

        # check if user has permission
        has_perm = RFQContractApproval.has_create_perm(user)

        # Return 403 if user does not have permission
        if not has_perm:
            return Response(
                {"message": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get profile of the current user
        profile = user.profile

        # start a database transaction
        with transaction.atomic():

            try:
                # Get actual contract and lock it for update
                contract = RFQContract.objects.select_for_update().get(pk=contract_id)

                # check if contract is in pending state
                if contract.approval_status != ApprovalChoices.PENDING:
                    raise ValueError("Contract is not in pending state.")

                # check if contract is already approved
                if contract.approval_record is not None:  # type: ignore
                    raise ValueError("Contract is already approved.")

            except RFQContract.DoesNotExist:
                # return 404 if contract does not exist
                return Response(
                    {"message": "Contract not found"}, status=status.HTTP_404_NOT_FOUND
                )

            except Exception as e:
                # return 400 if contract not in pending state
                return Response(
                    {
                        "message": str(e)
                        or "Something went wrong. Please try again later."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # get single negotiation based on contract and the vendor
            data: dict = request.data.copy()

            # Set officer and contract of this approval
            data["officer"] = profile
            data["contract"] = contract

            # serialize data
            serializer = self.get_serializer(data=data)

            # validate data
            if serializer.is_valid():

                # save the approval
                approval: RFQContractApproval = serializer.save()

                # serialize the newly created approval
                result_serializer = ContractApprovalRetrieveSerializer(
                    instance=approval
                )

                # return the newly created approval
                return Response(
                    {"data": result_serializer.data}, status=status.HTTP_201_CREATED
                )

            # return 400 if data is not valid
            else:
                error_message = get_serializer_error_message(serializer)
                return Response(
                    {
                        "message": error_message
                        or "Something went wrong. Please try again later."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
