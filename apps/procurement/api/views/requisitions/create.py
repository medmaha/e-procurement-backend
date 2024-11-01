from decimal import Decimal
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.procurement.api.serializers.requisition import (
    RequisitionCreateSerializer,
    RequisitionItemSerializer,
)
from apps.accounts.models import Account
from apps.organization.models.procurement_plan import Threshold
from apps.core.utilities.errors import get_serializer_error_message
from apps.procurement.models.requisition import Requisition


class RequisitionCreateView(CreateAPIView):
    serializer_class = RequisitionCreateSerializer

    def create(self, request, *args, **kwargs):

        try:

            data = request.data.copy()
            items = data.pop("items")

            total_cost = sum(
                [
                    Decimal(item.get("unit_cost", 0)) * Decimal(item.get("quantity", 0))
                    for item in items
                ]
            )

            if not total_cost:
                return Response(
                    {"message": "Total cost cannot be zero", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = RequisitionCreateSerializer(data=data)
            items_serializer = RequisitionItemSerializer(data=items, many=True)

            if serializer.is_valid() and items_serializer.is_valid():
                profile = request.user.profile
                with transaction.atomic():
                    requisition_items = items_serializer.save()
                    requisition: Requisition = serializer.save(  # type: ignore
                        officer=profile, remarks=request.data.get("remarks", "")
                    )

                    requisition.items.add(*requisition_items)

                    matrix = requisition.get_approval_matrix()

                    if matrix:
                        Requisition.objects.only("pk").filter(
                            pk=requisition.pk
                        ).update()
                        requisition.current_approval_step = (  # type: ignore
                            matrix.workflow.get_initial_step(requisition)
                        )
                        requisition.save()
                    else:
                        return Response(
                            {
                                "message": "Error! No approval-matrix found for this requisition",
                                "success": False,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # approval = requisition.approval_record  # type: ignore

                    # TODO: GPPA Threshold evaluation
                    # approval.procurement_method = matching_threshold.procurement_method
                    # approval.save()

                    return Response(
                        {"success": True},
                        status=status.HTTP_201_CREATED,
                    )

            return Response(
                {
                    "message": get_serializer_error_message(
                        serializer
                        if len(serializer.errors.keys())  # type: ignore
                        else items_serializer
                    ),
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"message": e.__str__(), "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
