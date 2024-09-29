from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from apps.accounts.api.serializer.permissions import PermissionSelectListSerializer

from apps.organization.models import (
    Staff,
    Unit,
    Department,
    DepartmentProcurementPlan,
    AnnualPlan,
    AnnualPlanApproval,
)

from apps.procurement.models import (
    RFQ,
    Requisition,
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    ProcurementRequisitionApproval,
    FinanceRequisitionApproval,
)
from apps.procurement.models.rfq_contract import (
    RFQContract,
    RFQContractAward,
    RFQContractApproval,
)
from apps.accounts.models.groups import AuthGroup


class PermissionSelectListView(ListAPIView):
    serializer_class = PermissionSelectListSerializer

    def get_queryset(self):
        models = [
            # Auth
            (AuthGroup, ("add", "change", "view")),
            # Organization
            (Staff, ("add", "change")),
            (Unit, ("add", "change", "view")),
            (Department, ("add", "change", "view")),
            # Organization Annual Plan
            (AnnualPlan, ("add",)),
            (AnnualPlanApproval, ("add",)),
            (DepartmentProcurementPlan, ("add", "change", "view")),
            # Procurement
            (RFQ, ("add", "change", "view")),
            (Requisition, ("add", "change", "view")),
            (UnitRequisitionApproval, ("add", "change", "view")),
            (DepartmentRequisitionApproval, ("add", "change", "view")),
            (ProcurementRequisitionApproval, ("add", "change", "view")),
            (FinanceRequisitionApproval, ("add", "change", "view")),
            # Procurement Contract
            (RFQContract, ("add", "change", "view")),
            (RFQContractAward, ("add", "change", "view")),
            (RFQContractApproval, ("add", "change", "view")),
        ]

        attr = [
            (model[0]._meta.app_label, model[0]._meta.model_name) for model in models
        ]

        app_labels, model_names = zip(*attr)
        app_labels = set(app_labels)

        contenttypes = ContentType.objects.filter(
            app_label__in=app_labels, model__in=model_names
        )

        permissions = Permission.objects.filter(content_type__in=contenttypes)
        # ).exclude(codename__regex=r"(?i)(view|user|delete)")

        return permissions

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
