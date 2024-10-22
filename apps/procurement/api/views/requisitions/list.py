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
    ProcurementMethodChoices,
)
from apps.procurement.models.requisition_approvals import (
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    FinanceRequisitionApproval,
    ProcurementRequisitionApproval,
)


class RequisitionListView(ListAPIView):
    serializer_class = RequisitionListSerializer

    def get_queryset(self):
        user: Account = self.request.user  # type: ignore
        profile_type, profile = user.get_profile()  # type: ignore

        if profile_type != "Staff":
            return None

        if user.groups.filter(name__icontains="admin").exists():
            queryset = Requisition.objects.prefetch_related("items")

        elif user.has_perm(
            f"{UnitRequisitionApproval._meta.app_label}.add_{UnitRequisitionApproval._meta.model_name}"
        ):
            queryset = Requisition.objects.filter(
                Q(officer=profile) | Q(officer__unit=profile.unit)
            ).prefetch_related("items")

        elif user.has_perm(
            f"{DepartmentRequisitionApproval._meta.app_label}.add_{DepartmentRequisitionApproval._meta.model_name}"
        ):
            # Get the requisition where the officer's department is equal to the user's department
            # And the "Unit" has already approve and accept the requisition
            queryset = Requisition.objects.filter(
                Q(
                    approval_record__unit_approval__isnull=False,
                    officer__unit__department=profile.unit.department,
                    approval_record__unit_approval__approve=ApprovalChoices.APPROVED,
                )
                | Q(officer=profile),
            ).prefetch_related("items")

        elif user.has_perm(
            f"{FinanceRequisitionApproval._meta.app_label}.add_{FinanceRequisitionApproval._meta.model_name}"
        ):
            # And the "Department" has already approve and accept the requisition
            queryset = Requisition.objects.filter(
                Q(
                    approval_record__department_approval__isnull=False,
                    approval_record__department_approval__approve=ApprovalChoices.APPROVED,
                )
                | Q(officer=profile)
            ).prefetch_related("items")

        elif user.has_perm(
            f"{ProcurementRequisitionApproval._meta.app_label}.add_{ProcurementRequisitionApproval._meta.model_name}"
        ):
            # And the "Finance" has approve and accept the requisition
            queryset = Requisition.objects.filter(
                Q(
                    approval_record__finance_approval__isnull=False,
                    approval_record__finance_approval__approve=ApprovalChoices.APPROVED,
                )
                | Q(officer=profile)
            ).prefetch_related("items")

        else:
            queryset = Requisition.objects.filter(officer=profile).prefetch_related(
                "items"
            )

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

        if "rfq" in self.request.query_params:  # type: ignore
            queryset = Requisition.objects.filter(
                approval_record__status=ApprovalChoices.APPROVED.value,
                approval_record__procurement_method__in=["rfq"],
                rfq__isnull=True,  # whether this requisition was recently used for rfq
            )
        else:
            queryset = Requisition.objects.filter(
                approval_record__status=ApprovalChoices.APPROVED.value,
                rfq__isnull=True,  # whether this requisition was recently used for rfq
            )
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {"data": response.data}
        return Response(data, status=status.HTTP_200_OK)
