from django.db import transaction
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response

from apps.core.utilities.errors import get_serializer_error_message
from apps.core.utilities.generators import revert_generated_unique_id
from apps.core.utilities.text_choices import ApprovalChoices, RFQLevelChoices
from apps.procurement.models.contract import Contract, Vendor, ContractAttachment
from apps.procurement.models import ContractAward, ContractAwardApproval
from apps.procurement.models.contract import ContractStatusChoices
from apps.procurement.models.contract_award import ContractAwardStatusChoices
from apps.vendors.models import RFQResponse
from apps.vendors.models.rfq_response import EvaluationStatusChoices


class ContractListSerializer(ModelSerializer):
    """
    Serializer for listing contract. This serializer is used in the
    """

    class Meta:
        model = Contract
        exclude = ["supplier", "attachments", "officer"]

    def to_representation(self, instance: Contract):
        """
        Custom representation for the ContractAward model. This method adds
        additional fields to the serialized data: officer and quotation.
        """
        data = super().to_representation(instance)

        # Add officer information to the serialized data
        data["attachments"] = instance.attachments.filter().values(
            "id", "name", "document_url", "uploaded_at"
        )

        data["supplier"] = {
            "id": instance.supplier.pk,
            "logo": instance.supplier.logo,
            "short_desc": instance.supplier.short_desc,
            "name": instance.supplier.organization_name,
        }

        data["officer"] = {
            "id": instance.officer.pk,
            "name": instance.officer.name,
            "job_title": instance.officer.job_title,
        }

        data["quotation"] = (
            {
                "id": instance.award.quotation.pk,
                "rfq_id": instance.award.quotation.rfq.pk,
                "delivery_date": instance.award.quotation.delivery_date,
                "created_date": instance.award.quotation.created_date,
                "pricing": instance.award.quotation.pricing,
                "evaluation_status": instance.award.quotation.evaluation_status,
                "vendor": {
                    "id": instance.award.quotation.vendor.pk,
                    "logo": instance.award.quotation.vendor.logo,
                    "name": instance.award.quotation.vendor.organization_name,
                    "short_desc": instance.award.quotation.vendor.short_desc,
                },
            }
            if instance.award
            else None
        )

        return data


class ContractCreateSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "title",
            "description",
            "terms_and_conditions",
            "start_date",
            "end_date",
            "payment_terms",
            "delivery_schedule",
            "penalty_clause",
        ]


class AttachmentsSerializer(ModelSerializer):
    class Meta:
        model = ContractAttachment
        read_only_fields = ["id", "uploaded_at"]
        fields = ["id", "name", "document_url", "uploaded_at"]


class ContractListAPIView(APIView):

    def get_queryset(self, profile_type, profile, contract_id=None):
        if profile_type == "Staff":
            if contract_id:
                queryset = Contract.objects.get(pk=contract_id)
            else:
                queryset = Contract.objects.filter()
        elif profile_type == "Vendor":
            if contract_id:
                queryset = Contract.objects.get(pk=contract_id)
            else:
                queryset = Contract.objects.filter()
        else:
            if contract_id:
                queryset = Contract.objects.get(pk=contract_id)
            else:
                queryset = Contract.objects.filter()
        return queryset

    def get(self, request, contract_id=None, *args, **kwargs):
        try:
            profile_type, profile = request.user.get_profile()

            queryset = self.get_queryset(
                profile_type, profile, revert_generated_unique_id(None, contract_id)
            )
            serializer = ContractListSerializer(queryset, many=contract_id is None)

            return Response({"data": serializer.data})
        except Exception as e:
            return Response(str(e), status=400)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        _supplier = data.get("supplier")

        if not _supplier:
            return Response(
                {"message": "Please provide a valid supplier."},
                status=400,
            )

        attachments = data.get("attachments")
        attachments_serializer = None
        if attachments:
            attachments_serializer = AttachmentsSerializer(data=attachments, many=True)
            if not attachments_serializer.is_valid():
                error_message = get_serializer_error_message(attachments_serializer)
                return Response(
                    {"message": error_message},
                    status=400,
                )

        _award = data.get("award", None)
        try:
            supplier = Vendor.objects.get(
                pk=revert_generated_unique_id(None, _supplier)
            )
            if _award:
                award = ContractAward.objects.get(
                    pk=revert_generated_unique_id(None, _award)
                )
                if award.contract:  # type: ignore
                    return Response(
                        {
                            "message": "Award is already associated with contract.",
                        },
                        status=403,
                    )
            with transaction.atomic():
                serializer = ContractCreateSerializer(data=data)
                if serializer.is_valid():
                    profile = request.user.profile
                    contract: Contract = serializer.save(  # type: ignore
                        officer=profile,
                        award=award,
                        supplier=supplier,
                    )
                    if attachments_serializer:
                        attachments = attachments_serializer.save()
                        contract.attachments.set(attachments)

                    contract_serializer = ContractCreateSerializer(contract)
                    return Response(
                        {"data": contract_serializer.data},
                        status=201,
                    )
                error_message = get_serializer_error_message(serializer)
                return Response(
                    {"message": error_message},
                    status=400,
                )

        except Exception as e:
            return Response({"message": e.__str__()}, status=500)

    def put(self, request, contract_id, *args, **kwargs):

        contract = Contract.objects.get(
            pk=revert_generated_unique_id(None, contract_id)
        )

        if contract.status != ContractStatusChoices.DRAFT:
            return Response(
                {"message": "Only contracts draft status can be updated."},
                status=400,
            )

        data = request.data.copy()
        _supplier = data.get("supplier")

        if not _supplier:
            return Response(
                {"message": "Please provide a valid supplier."},
                status=400,
            )

        attachments = data.get("attachments")
        attachments_serializer = None
        if attachments:
            attachments_serializer = AttachmentsSerializer(data=attachments, many=True)
            if not attachments_serializer.is_valid():
                error_message = get_serializer_error_message(attachments_serializer)
                return Response(
                    {"message": error_message},
                    status=400,
                )

        _award = data.get("award", None)
        try:
            supplier = Vendor.objects.get(
                pk=revert_generated_unique_id(None, _supplier)
            )
            if _award:
                award = ContractAward.objects.get(
                    pk=revert_generated_unique_id(None, _award)
                )
                if award.contract and award.contract != contract:  # type: ignore
                    return Response(
                        {
                            "message": "Award is already associated with contract.",
                        },
                        status=403,
                    )
            with transaction.atomic():
                serializer = ContractCreateSerializer(contract, data=data)
                if serializer.is_valid():
                    profile = request.user.profile
                    contract: Contract = serializer.save(  # type: ignore
                        officer=profile,
                        award=award,
                        supplier=supplier,
                    )
                    if attachments_serializer:
                        attachments = attachments_serializer.save()
                        contract.attachments.set(attachments)

                    contract_serializer = ContractCreateSerializer(contract)
                    return Response(
                        {
                            "data": contract_serializer.data,
                            "message": "Contract updated",
                        },
                        status=200,
                    )
                error_message = get_serializer_error_message(serializer)
                return Response(
                    {"message": error_message},
                    status=400,
                )

        except Exception as e:
            return Response({"message": e.__str__()}, status=500)
