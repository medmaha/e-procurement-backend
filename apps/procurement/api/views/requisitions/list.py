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
from apps.core.utilities.text_choices import (
    ApprovalChoices,
)


class RequisitionListView(ListAPIView):
    serializer_class = RequisitionListSerializer

    def get_queryset(self):
        user: Account = self.request.user  # type: ignore
        profile_type, profile = user.get_profile()  # type: ignore

        if profile_type != "Staff":
            return None

        if user.groups.filter(name__icontains="admin").exists():
            queryset = Requisition.objects.all()

        elif user.has_perm("procurement.add_unitrequisitionapproval"):
            queryset = Requisition.objects.filter(
                Q(officer__unit=profile.unit) | Q(officer=profile)
            )
        elif user.has_perm("procurement.add_departmentrequisitionapproval"):
            queryset = Requisition.objects.filter(
                Q(
                    officer__unit__department=profile.unit.department,
                    approval_record__unit_approval__isnull=False,
                )
                | Q(officer=profile),
            )
        elif user.has_perm("procurement.add_procurementrequisitionapproval"):
            queryset = Requisition.objects.filter(
                Q(
                    approval_record__unit_approval__isnull=False,
                    approval_record__department_approval__isnull=False,
                )
                | Q(officer=profile)
            )
        elif user.has_perm("procurement.add_financerequisitionapproval"):
            queryset = Requisition.objects.filter(
                Q(
                    approval_record__unit_approval__isnull=False,
                    approval_record__department_approval__isnull=False,
                    approval_record__procurement_approval__isnull=False,
                )
                | Q(officer=profile)
            )
        else:
            queryset = Requisition.objects.filter(officer=profile)

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        auth_perms = {
            "create": request.user.has_perm("procurement.add_requisition"),
            "read": request.user.has_perm("procurement.view_requisition"),
            "update": request.user.has_perm("procurement.change_requisition"),
            "delete": request.user.has_perm("procurement.delete_requisition"),
        }

        data = {"data": response.data, "auth_perms": auth_perms}

        return Response(data, status=status.HTTP_200_OK)


class RequisitionSelectView(ListAPIView):
    serializer_class = RequisitionSelectSerializer

    def get_queryset(self):
        user: Account = self.request.user  # type: ignore
        profile_name, profile = user.get_profile()  # type: ignore

        queryset = Requisition.objects.filter(
            approval_record__status=ApprovalChoices.ACCEPTED.value,
            approval_record__procurement_method__in=["rfq", "rfq 2"],
            rfq__isnull=True,  # whether this requisition was recently used for rfq
        )
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {"data": response.data}
        return Response(data, status=status.HTTP_200_OK)
