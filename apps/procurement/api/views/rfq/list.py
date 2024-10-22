from datetime import date
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from apps.procurement.models import RFQ
from apps.procurement.api.serializers.rfq import (
    RFQListSerializer,
    RFQSelectSerializer,
)
from apps.accounts.models import Account
from apps.core.utilities.text_choices import ApprovalChoices


class RfqListView(ListAPIView):
    serializer_class = RFQListSerializer

    def get_queryset(self):
        user: Account = self.request.user  # type: ignore
        profile_name, profile = user.get_profile()  # type: ignore
        queryset = RFQ.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)

        # CRUD permissions
        auth_perms = {
            "create": request.user.has_perm("procurement.add_rfq"),
            "read": request.user.has_perm("procurement.view_rfq"),
            "update": request.user.has_perm("procurement.change_rfq"),
            "delete": request.user.has_perm("procurement.delete_rfq"),
        }
        data = {"data": serializer.data, "auth_perms": auth_perms}
        return Response(data, status=status.HTTP_200_OK)


class RfqSelectView(ListAPIView):
    serializer_class = RFQSelectSerializer

    def get_queryset(self):
        user: Account = self.request.user  # type: ignore
        profile_name, profile = user.get_profile()  # type: ignore

        queryset = RFQ.objects.filter(
            approval_record__approve=ApprovalChoices.APPROVED.value
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        auth_perms = {
            "create": request.user.has_perm("procurement.add_rfqapproval"),
            "read": request.user.has_perm("procurement.view_rfqapproval"),
            "update": request.user.has_perm("procurement.change_rfqapproval"),
            "delete": request.user.has_perm("procurement.delete_rfqapproval"),
        }

        data = {"data": serializer.data, "auth_perms": auth_perms}
        return Response(data, status=status.HTTP_200_OK)
