from datetime import date
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required
from apps.core.decorators.permissions import staff_view

from apps.procurement.forms import RequisitionApprovalForm
from apps.procurement.models import RequisitionApproval
from apps.procurement.models.requisition_approvals import (
    DepartmentRequisitionApproval,
    FinanceRequisitionApproval,
    ProcurementRequisitionApproval,
    UnitRequisitionApproval,
)


@login_required
@staff_view
def approve_detail(request, id):
    error_message = None
    success_message = None
    profile = request.user.profile

    approval = get_object_or_404(RequisitionApproval, approval_id=id)

    form = RequisitionApprovalForm(instance=approval)
    procurement_plans = []

    permissions = request.permissions

    user_approval = None
    finance = False

    if permissions["procurement"].get("UNIT_REQ_APPROVAL"):
        user_approval = UnitRequisitionApproval
    if permissions["procurement"].get("DEPARTMENT_REQ_APPROVAL"):
        user_approval = DepartmentRequisitionApproval
    if permissions["procurement"].get("FINANCE_REQ_APPROVAL"):
        user_approval = FinanceRequisitionApproval
        finance = True
    if permissions["procurement"].get("PROCUREMENT_REQ_APPROVAL"):
        user_approval = ProcurementRequisitionApproval

    if user_approval:
        user_approval = user_approval.objects.filter(
            officer=request.user.profile, requisition_number=approval.requisition.requisition_number  # type: ignore
        ).first()

    context = {
        "form": form,
        "approval": approval,
        "finance": finance,
        "plans": procurement_plans,
        "user_approval": user_approval,
        "error_message": error_message,
        "success_message": success_message,
    }

    template_url = "procurement/requisitions/approve/detail.html"

    return render(
        request,
        template_url,
        context=context,
        status=200 if not error_message else 400,
    )
