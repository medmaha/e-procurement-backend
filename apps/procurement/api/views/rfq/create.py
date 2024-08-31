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
        profile_name, profile = user.get_profile()

        data: Any = request.data.copy()

        if not data.get("required_date"):
            return Response(
                {
                    "message": "Error! RFQ requires a deadline date.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        requisition = get_object_or_404(
            Requisition,
            pk=data.pop("requisition_id") if "requisition_id" in data else 0,
        )

        e_404 = "RFQ requires at least one supplier."
        e_kwargs = {"message": e_404}
        suppliers = (
            get_list_or_404(Vendor, pk__in=data.pop("suppliers"))
            if "suppliers" in data
            else None
        )
        if not suppliers:
            return Response(
                e_kwargs,
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_serializer = (
            RFQItemsCreateSerializer(data=data.pop("items"), many=True)
            if "items" in data
            else None
        )

        if not items_serializer or not items_serializer.is_valid():
            return Response(
                {
                    "message": "RFQ requires at least one item to quote.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        conditions = data.pop("conditions") if "conditions" in data else ""
        auto_publish = data.get("auto_publish") == "on"

        data.update({"auto_publish": auto_publish, "terms_and_conditions": conditions})

        rfq_serializer: Any = RFQCreateSerializer(
            data=data, context={"request": request}
        )

        if rfq_serializer.is_valid():
            with transaction.atomic():
                rfq: RFQ = rfq_serializer.save(officer=profile, requisition=requisition)
                items_serializer.save(rfq=rfq)
                rfq.suppliers.set(suppliers)

                staff_ids = request.data.get("staff_ids")
                if isinstance(staff_ids, list):
                    try:
                        for i, s in enumerate(staff_ids):
                            staff_ids[i] = int(s)
                    except:
                        staff_ids = None
                else:
                    staff_ids = None

                if staff_ids:
                    accounts = Account.objects.filter(
                        groups__in=Group.objects.filter(id__in=staff_ids)
                    )
                else:
                    accounts = Account.objects.filter(
                        groups__in=Group.objects.filter(
                            name__iexact="RFQ Response Opener"
                        )
                    )
                opened_by_staffs = Staff.objects.filter(user_account__in=accounts)
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
