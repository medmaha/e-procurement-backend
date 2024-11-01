from typing import Any
from django.db import transaction
from django.db.models import Subquery
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.procurement.api.serializers.rfq import (
    RFQCreateSerializer,
    RFQItemsCreateSerializer,
)
from apps.vendors.models.vendor import Vendor
from apps.procurement.models import Requisition
from apps.core.utilities.errors import get_serializer_error_message
from apps.organization.models.staff import Staff
from apps.procurement.models.rfq import RFQ
from apps.accounts.models.account import Account


class RFQCreateView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile

        data: Any = request.data.copy()

        if not data.get("required_date"):
            return Response(
                {
                    "message": "Error! RFQ requires a deadline date.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        requisition = Requisition.objects.only("pk").get(pk=data.pop("requisition_id"))

        e_404 = "RFQ requires at least one supplier."
        e_kwargs = {"message": e_404}

        suppliers_ids = data.pop("suppliers")

        if not (suppliers_ids and isinstance(suppliers_ids, list)):
            return Response(
                e_kwargs,
                status=status.HTTP_400_BAD_REQUEST,
            )

        suppliers = get_list_or_404(Vendor, pk__in=suppliers_ids)

        if not suppliers:
            return Response(
                e_kwargs,
                status=status.HTTP_400_BAD_REQUEST,
            )

        rfq_items_data = data.pop("items", None)

        if not rfq_items_data:
            return Response(
                {
                    "message": "RFQ requires at least one item to quote. AA",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_serializer = RFQItemsCreateSerializer(data=rfq_items_data, many=True)

        if not items_serializer.is_valid():
            return Response(
                {
                    "message": "RFQ requires at least one item to quote. BB",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        terms_and_conditions = data.pop("conditions") if "conditions" in data else ""
        auto_publish = data.get("auto_publish", None) in ["on", "true", True]

        data.update(
            {"auto_publish": auto_publish, "terms_and_conditions": terms_and_conditions}
        )

        data["quotation_deadline_date"] = data.get("required_date")

        rfq_serializer: Any = RFQCreateSerializer(
            data=data, context={"request": request}
        )

        if rfq_serializer.is_valid():
            with transaction.atomic():
                rfq: RFQ = rfq_serializer.save(officer=profile, requisition=requisition)
                items_serializer.save(rfq=rfq)
                rfq.suppliers.set(suppliers)

                opened_by_accounts = Account.objects.only("pk").filter(
                    groups__in=Group.objects.filter(name__iexact="RFQ Response Opener")
                )

                opened_by_staffs = None
                if opened_by_accounts:
                    opened_by_staffs = Staff.objects.only("pk").filter(
                        user_account__in=opened_by_accounts
                    )

                if opened_by_staffs:
                    rfq.opened_by.set(opened_by_staffs)

                return Response(
                    {
                        "message": "RFQ created successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {
                "message": "Oops! sorry, something went wrong. %s"
                % get_serializer_error_message(rfq_serializer)
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
