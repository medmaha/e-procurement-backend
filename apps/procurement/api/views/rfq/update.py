from typing import Any
from django.db import transaction
from django.db.models import Subquery
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

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
from apps.core.utilities.generators import revert_generated_unique_id
from apps.core.utilities.text_choices import RFQLevelChoices


class RFUpdateView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        user = request.user
        profile_name, profile = user.get_profile()

        if profile_name != "Staff":
            return Response(
                {"message": "Permission denied! Only staff can update RFQ."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rfq = get_object_or_404(
            RFQ, pk=revert_generated_unique_id(None, request.data.get("rfq_id"))
        )
        if rfq.level != RFQLevelChoices.APPROVAL_LEVEL.value:
            return Response(
                {"message": "This RFQ cannot be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if rfq.officer != profile:
            return Response(
                {"message": "Permission denied! Only RFQ officer can update this RFQ."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        items_serializer = RFQItemsCreateSerializer(data=data.get("items"), many=True)
        if not items_serializer.is_valid():
            return Response(
                {
                    "message": get_serializer_error_message(items_serializer),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        conditions = data.pop("conditions") if "conditions" in data else ""
        auto_publish = data.get("auto_publish") == "on"
        data.update({"auto_publish": auto_publish, "terms_and_conditions": conditions})
        rfq_serializer: Any = RFQCreateSerializer(
            instance=rfq, data=data, context={"request": request}
        )
        if not rfq_serializer.is_valid():
            return Response(
                {"message": get_serializer_error_message(rfq_serializer)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            rfq: RFQ = rfq_serializer.save(officer=profile, requisition=requisition)
            rfq.items.delete()
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
                # TODO: Make the rfq opener group name a constant variable
                accounts = Account.objects.filter(
                    groups__in=Group.objects.filter(name__iexact="RFQ Response Opener")
                )
            opened_by_staffs = Staff.objects.filter(user_account__in=accounts)
            rfq.opened_by.set(opened_by_staffs)
            return Response(
                {
                    "message": "RFQ updated successfully",
                },
                status=status.HTTP_201_CREATED,
            )
