from itertools import count
import re
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.procurement.api.serializers.quotations import (
    RFQResponseListSerializer,
    RFQRespondSelectSerializer,
)
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.text_choices import ApprovalChoices
from apps.core.utilities.generators import revert_unique_id, generate_unique_id
from apps.procurement.models.rfq import RFQ


class QuotationRespondListView(ListAPIView):
    def get_queryset(self, query_params):
        rfq = query_params.get("rfq", None)
        year = query_params.get("year", None)
        search: str = query_params.get("search", None)
        search_includes_rfq = ("rfq" in search or "RFQ" in search) if search else False
        should_filter = bool(rfq) or bool(year) or bool(search)
        filtered = False

        query = {}
        query_all = False

        if str(rfq).lower() == "all":
            query_all = True
            should_filter = False

        first_fetch = not should_filter and not query_all

        if first_fetch:
            query.update({"rfq": RFQ.objects.order_by("-id").first()})

        queryset = RFQResponse.objects.filter(**query)

        if first_fetch and not queryset.count():
            queryset = RFQResponse.objects.filter()

        if str(rfq).lower() == "latest":
            qs = queryset.filter(rfq=RFQ.objects.order_by("-id").first())
            queryset = qs
            filtered = qs.exists()

        if str(rfq).lower() == "oldest":
            qs = queryset.filter(rfq=RFQ.objects.order_by("id").first())
            queryset = qs
            filtered = qs.exists()

        if search:
            if search_includes_rfq:
                qs = queryset.filter(rfq__id=revert_unique_id("", search))
                queryset = qs
                filtered = qs.exists()
            elif re.search("[a-zA-Z]", search):
                qs = queryset.filter(
                    Q(vendor__organization_name__icontains=search)
                    | Q(vendor__alias__icontains=search)
                )
                queryset = qs
                filtered = qs.exists()
            else:
                qs = queryset.filter(Q(id=revert_unique_id("", search)))
                queryset = qs
                filtered = qs.exists()
        if year:
            try:
                qs = queryset.filter(created_date__year=int(year))
                queryset = qs
                filtered = qs.exists()
            except:
                pass

        if should_filter and not filtered:
            return []

        return queryset[:10]

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        queryset = self.get_queryset(request.query_params)

        def func(queryset):
            return bool(queryset)

        serializer = RFQResponseListSerializer(
            list(queryset), many=True, context={"request": request, "slim": False}
        )
        # queryset = filter(func, serializer.data)

        auth_perms = {
            "create": request.user.has_perm("vendors.add_rfqresponse"),
            "read": request.user.has_perm("vendors.view_rfqresponse"),
            "update": request.user.has_perm("vendors.change_rfqresponse"),
            "delete": request.user.has_perm("vendors.delete_rfqresponse"),
        }

        return Response(
            {
                # "data": queryset,
                "data": serializer.data,
                "auth_perms": auth_perms,
            },
            status=status.HTTP_200_OK,
        )


class QuotationRespondSelectView(ListAPIView):
    serializer_class = RFQRespondSelectSerializer

    def get_queryset(self, profile_type):
        if profile_type == "Vendor":
            "Selecting Quotes for invoicing"
            return RFQResponse.objects.filter(
                status=ApprovalChoices.ACCEPTED.value, evaluation_status="accepted"
            )

        "Selecting Quotes for evaluation or purchase orders"
        return RFQResponse.objects.filter(
            status=ApprovalChoices.ACCEPTED.value, evaluation_status="processing"
        )

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        queryset = self.get_queryset(profile_type)
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )
