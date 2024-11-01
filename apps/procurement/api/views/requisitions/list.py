from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from apps.procurement.models import Requisition
from apps.procurement.api.serializers.requisition import (
    RequisitionListSerializer,
    RequisitionSelectSerializer,
)
from apps.accounts.models import Account
from apps.core.utilities.text_choices import ApprovalChoices, PRStatusChoices


class RequisitionListView(ListAPIView):
    serializer_class = RequisitionListSerializer

    def get_queryset(self):
        user: Account = self.request.user  # type: ignore
        profile_type, profile = user.get_profile()  # type: ignore

        if profile_type != "Staff":
            return None

        queryset = (
            Requisition.objects.prefetch_related(
                "items",
                "approval_actions",
                "officer",
                "current_approval_step",
            )
            .filter(
                Q(officer=profile)  # The requisition is created by the user
                | Q(
                    current_approval_step__step__approver=profile
                )  # The requisitions approved by this user
                | Q(
                    approval_actions__approver=profile
                )  # The requisitions that needs this user's to approve
            )
            .distinct()
        )

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        auth_perms = {
            "create": request.user.has_perm(
                f"{Requisition._meta.app_label}.add_{Requisition._meta.model_name}"
            ),
            "read": request.user.has_perm(
                f"{Requisition._meta.app_label}.view_{Requisition._meta.model_name}"
            ),
            "update": request.user.has_perm(
                f"{Requisition._meta.app_label}.change_{Requisition._meta.model_name}"
            ),
            "delete": request.user.has_perm(
                f"{Requisition._meta.app_label}.delete_{Requisition._meta.model_name}"
            ),
        }

        data = {"data": response.data, "auth_perms": auth_perms}

        return Response(data, status=status.HTTP_200_OK)


class RequisitionSelectView(ListAPIView):
    serializer_class = RequisitionSelectSerializer

    def get_queryset(self):
        if "rfq" in self.request.query_params:  # type: ignore
            queryset = Requisition.objects.prefetch_related("items").filter(
                pr_status=PRStatusChoices.PENDING,
                approval_status=ApprovalChoices.APPROVED,
            )
        else:
            queryset = Requisition.objects.prefetch_related("items").filter()
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {"data": response.data}
        return Response(data, status=status.HTTP_200_OK)
