from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response

from apps.core.utilities.text_choices import ApprovalChoices, RFQLevelChoices
from apps.procurement.models.contract import Contract
from apps.procurement.models import ContractAward, ContractAwardApproval
from apps.procurement.models.contract_award import ContractAwardStatusChoices
from apps.vendors.models import RFQResponse
from apps.vendors.models.rfq_response import EvaluationStatusChoices


class ContractAwardListSerializer(ModelSerializer):
    """
    Serializer for listing contract awards. This serializer is used in the
    ContractAwardListAPIView
    """

    class Meta:
        model = ContractAward
        fields = ["id", "status", "remarks", "created_date", "last_modified"]

    def to_representation(self, instance: ContractAward):
        """
        Custom representation for the ContractAward model. This method adds
        additional fields to the serialized data: officer and quotation.
        """
        data = super().to_representation(instance)

        # Add officer information to the serialized data
        data["officer"] = {
            "id": instance.officer.pk,
            "name": instance.officer.name,
            "job_title": instance.officer.job_title,
        }

        approval: ContractAwardApproval = instance.approval  # type: ignore

        data["approval"] = {
            "id": approval.pk,
            "officer": (
                {
                    "id": instance.officer.pk,
                    "name": instance.officer.name,
                    "job_title": instance.officer.job_title,
                }
                if approval
                else None
            ),
            "approve": approval.approve,
            "created_date": approval.created_date,  # type: ignore
        }

        # Add quotation information to the serialized data
        data["quotation"] = {
            "id": instance.quotation.pk,
            "rfq_id": instance.quotation.rfq.pk,
            "delivery_date": instance.quotation.delivery_date,
            "created_date": instance.quotation.created_date,
            "pricing": instance.quotation.pricing,
            "evaluation_status": instance.quotation.evaluation_status,
            "vendor": {
                "id": instance.quotation.vendor.pk,
                "logo": instance.quotation.vendor.logo,
                "name": instance.quotation.vendor.organization_name,
                "short_desc": instance.quotation.vendor.short_desc,
            },
        }

        return data


class ContractAwardListAPIView(GenericAPIView):
    serializer_class = ContractAwardListSerializer

    def get(self, request, *args, **kwargs):
        """
        GET request handler. Lists all contract awards. The response is filtered
        based on the user's profile type.
        """
        profile_type, profile = request.user.get_profile()

        if profile_type == "Staff":
            # Staff should see all contract awards
            queryset = ContractAward.objects.select_related(
                "quotation", "quotation__rfq", "officer"
            ).filter()

        elif profile_type == "Vendor":
            # Vendors should only see their own contract awards
            queryset = ContractAward.objects.select_related(
                "quotation", "quotation__rfq", "officer", "quotation__vendor"
            ).filter(
                status=ContractAwardStatusChoices.AWARDED,
                quotation__vendor__id=profile.pk,
            )

        else:
            # Other users should not see any contract awards
            queryset = []

        serializer = self.get_serializer(queryset, many=True)

        print(request.user)
        auth_perms = {
            "create": Contract.has_create_perm(request.user),
            "approve": ContractAwardApproval.has_create_perm(request.user),
        }

        print(auth_perms)

        return Response({"data": serializer.data, "auth_perms": auth_perms})

    def post(self, request, *args, **kwargs):
        """
        POST request handler. Creates a new contract award. The request is
        validated based on the user's profile type.
        """
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            # Staff cannot create contract awards
            return Response(
                {
                    "message": "Forbidden Request",
                },
                status=403,
            )

        try:
            with transaction.atomic():

                # Get the quotation id from the request data
                quotation_id = request.data.get("quotation")

                # Get the quotation object from the database
                quotation = (
                    RFQResponse.objects.select_for_update()
                    .only("id", "rfq__id", "rfq__level")
                    .get(id=quotation_id)
                )

                # Make sure the RFQ-level is not on Award-Level
                if quotation.rfq.level == RFQLevelChoices.AWARD_LEVEL:
                    return Response(
                        {
                            "message": "RFQ already awarded",
                        },
                        status=403,
                    )

                # Check if a contract award already exists for the quotation
                existing_award = (
                    ContractAward.objects.only("id")
                    .filter(quotation=quotation)
                    .exists()
                )

                if existing_award:
                    # If a contract award already exists, return an error
                    return Response(
                        {
                            "message": "Quotation was already awarded",
                        },
                        status=403,
                    )

                # Check if an existing quotation from this quotation's rfq was ever award and approve
                existing_quotation_award = (
                    ContractAward.objects.only(
                        "quotation__rfq__id", "approval__approve"
                    )
                    .filter(quotation__rfq__id=quotation.rfq.pk)
                    .filter(approval__approve=ApprovalChoices.APPROVED)
                    .exists()
                )

                # If a contract award already exists, return an error
                if existing_quotation_award:
                    return Response(
                        {
                            "message": "RFQ already awarded",
                        },
                        status=403,
                    )

                # Create a new contract award
                award = ContractAward(
                    quotation=quotation,
                    officer=profile,
                    remarks=request.data.get("remarks", ""),
                )

                award.full_clean()  # Validate the contract award
                award.save()  # Save the award
                quotation.evaluation_status = (
                    EvaluationStatusChoices.AWARD_AWAITING_APPROVAL
                )
                quotation.save()
                quotation.rfq.level = RFQLevelChoices.AWARD_LEVEL
                quotation.rfq.save()

                # TODO: Notify the authorized approve about this award decision.

                serializer = self.get_serializer(award)  # Serialize the contract award

                # Return the serialized data
                return Response(
                    {
                        "data": serializer.data,
                    },
                    status=201,
                )

        except RFQResponse.DoesNotExist:
            # If the quotation does not exist, return an error
            return Response(
                {
                    "message": "Quotation does not exists",
                },
                status=404,
            )

        except Exception as e:
            # If an unhandled exception occurs, return an error
            return Response(
                {
                    "message": str(e) or "Unhandled Internal Server Error",
                },
                status=500,
            )

    def put(self, request, award_id, *args, **kwargs):
        """
        PUT request handler. Creates a new contract award. The request is
        validated based on the user's profile type.
        """
        profile_type, profile = request.user.get_profile()

        if profile_type != "Staff":
            # Staff cannot create contract awards
            return Response(
                {
                    "message": "Forbidden Request",
                },
                status=403,
            )

        # TODO: Determine the user's permission

        try:

            if not "approval_mode" in request.data:
                return Response(
                    {"data": {}},
                    status=200,
                )

            with transaction.atomic():

                # Attempt to get the award from the database
                award = ContractAward.objects.select_for_update().get(id=award_id)

                # To proceed with this request,
                # the status of this award should be in pending state
                if award.status != ContractAwardStatusChoices.PENDING:
                    return Response(
                        {
                            "message": f'This award was already processed and "{award.status}"',
                        },
                        status=403,
                    )

                # Check if an existing contract award-approval already exists
                existing_approval = ContractAwardApproval.objects.filter(
                    award=award
                ).exists()

                # Return an error if an existing contract award-approval already exists
                if existing_approval:
                    return Response(
                        {
                            "message": f'This award was already processed and "{award.status}"',
                        },
                        status=403,
                    )

                # set contract-award status based on the request data
                approved = request.data.get("approve") in ["true", True]
                if approved:
                    award.status = ContractAwardStatusChoices.AWARDED
                else:
                    award.status = ContractAwardStatusChoices.REJECTED

                # set the appropriate approve-status base on the request data
                approval_status = (
                    ApprovalChoices.APPROVED if approved else ApprovalChoices.REJECTED
                )

                # Create a new contract award-approval
                approval = ContractAwardApproval(
                    award=award,
                    approver=profile,
                    approve=approval_status,
                )

                # Update the contract award-approval
                approval.remarks = request.data.get("remarks", "")
                approval.save()
                award.save()

                # Update status of the quotation this award links to
                award.quotation.evaluation_status = (
                    EvaluationStatusChoices.AWARDED
                    if approved
                    else EvaluationStatusChoices.REJECTED
                )
                # Update status of the rfq this award's quotation links to
                award.quotation.rfq.level = RFQLevelChoices.CONTRACT_LEVEL

                # Save changes
                award.quotation.save()
                award.quotation.rfq.save()

                # Serialize the contract award
                serializer = self.serializer_class(approval.award)

                # Return the serialized data
                return Response(
                    {
                        "data": serializer.data,
                    },
                    status=200,
                )

        except ContractAward.DoesNotExist:
            # If the quotation does not exist, return an error
            return Response(
                {
                    "message": "Award does not exists",
                },
                status=404,
            )

        except Exception as e:
            # If an unhandled exception occurs, return an error
            return Response(
                {
                    "message": str(e) or "Unhandled Internal Server Error",
                },
                status=500,
            )
