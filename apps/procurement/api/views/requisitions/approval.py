from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, get_object_or_404

from apps.accounts.models import Account
from apps.procurement.api.serializers.requisition import RequisitionApprovalSerializer
from apps.procurement.models.requisition_approval import RequisitionApproval
from apps.procurement.models.requisition_approvals import (
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    FinanceRequisitionApproval,
    ProcurementRequisitionApproval,
)
from apps.organization.models.procurement_plan import PlanItem
from apps.core.utilities.text_choices import ApprovalChoices


class RequisitionApprovalView(UpdateAPIView):
    serializer_class = RequisitionApprovalSerializer

    models = {
        "unit_approval": UnitRequisitionApproval,
        "department_approval": DepartmentRequisitionApproval,
        "procurement_approval": ProcurementRequisitionApproval,
        "finance_approval": FinanceRequisitionApproval,
    }

    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        approval: RequisitionApproval = get_object_or_404(
            RequisitionApproval, pk=request.data.get("approval_id")
        )

        STAGE = approval.stage.lower()
        if not STAGE:
            return Response(
                {"message": "This requisition is disable for approval"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record_data = request.data.get(STAGE)
        STAGE_NAME = STAGE + "_approval"

        if not "approve" in record_data:
            return Response(
                {"message": "Error! Requisition approval not present"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        approved = record_data.get("approve") == "on"
        record_data["approve"] = (
            ApprovalChoices.APPROVED.value
            if approved
            else ApprovalChoices.REJECTED.value
        )

        if record_data:
            if STAGE == "procurement":
                plan_id = record_data.get("annual_procurement_plan")
                annual_procurement_plan = (
                    get_object_or_404(PlanItem, pk=plan_id) if plan_id else None
                )
                record_data["part_of_annual_plan"] = annual_procurement_plan is not None
                record_data["annual_procurement_plan"] = annual_procurement_plan

            model = self.models[STAGE_NAME]
            record = model.objects.create(
                **record_data,
                officer=profile,
            )
            setattr(approval, STAGE_NAME, record)
            approval.save()

            return Response(
                {"message": "Requisition Approval updated"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Error! Requisition Approval not updated"},
            status=status.HTTP_400_BAD_REQUEST,
        )
