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


class RequisitionCreateView(CreateAPIView):
    serializer_class = RequisitionCreateSerializer

    def create(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        data = request.data.copy()

        try:
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

            matching_threshold = Threshold.get_matching_threshold(total_cost)
            if not matching_threshold:
                return Response(
                    {
                        "message": "The total price is not in the GPPA threshold range",
                        "success": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(e)
            return Response(
                {"message": 'Required field "items" is missing', "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RequisitionCreateSerializer(data=data)
        items_serializer = RequisitionItemSerializer(data=items, many=True)

        if serializer.is_valid() and items_serializer.is_valid():
            with transaction.atomic():
                requisition_items = items_serializer.save()
                requisition = serializer.save(
                    officer=profile, remarks=request.data.get("remarks", "")
                )
                requisition.items.add(*requisition_items)  # type: ignore

                approval = requisition.approval_record  # type: ignore
                approval.procurement_method = matching_threshold.procurement_method
                approval.save()

                return Response(
                    {"success": True},
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {
                "message": get_serializer_error_message(serializer),
                "success": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
