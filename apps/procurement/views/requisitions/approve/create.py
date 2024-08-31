from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from apps.core.decorators.permissions import create_requisition_approval, staff_view
from django.contrib.auth.decorators import login_required
from apps.procurement.models.requisition_approvals import (
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    FinanceRequisitionApproval,
    ProcurementRequisitionApproval,
)
from apps.procurement.models.requisition_approval import RequisitionApproval


@login_required
@staff_view
@create_requisition_approval
def approve_create(request, id):
    approval = get_object_or_404(RequisitionApproval, approval_id=id)
    requisition_number = approval.requisition.requisition_number  # type: ignore
    perm_name = request.POST.get("perm_name")

    if perm_name == "UNIT_REQ_APPROVAL":
        appr, _ = UnitRequisitionApproval.objects.get_or_create(
            requisition_number=requisition_number, officer=request.user.profile
        )
        appr.remark = request.POST.get("remark", "")
        appr.approve_status = request.POST.get("status", "no")
        appr.save()
        approval.unit_approval = appr
        approval.save()
    elif perm_name == "DEPARTMENT_REQ_APPROVAL":
        appr, _ = DepartmentRequisitionApproval.objects.get_or_create(
            requisition_number=requisition_number, officer=request.user.profile
        )
        appr.remark = request.POST.get("remark", "")
        appr.approve_status = request.POST.get("status", "no")
        appr.save()
        approval.department_approval = appr
        approval.save()
    elif perm_name == "PROCUREMENT_REQ_APPROVAL":
        appr, _ = ProcurementRequisitionApproval.objects.get_or_create(
            requisition_number=requisition_number, officer=request.user.profile
        )
        appr.remark = request.POST.get("remark", "")
        appr.approve_status = request.POST.get("status", "no")
        appr.requisition_number = requisition_number
        appr.save()
        approval.procurement_requisition_approval = appr
        approval.save()
    elif perm_name == "FINANCE_REQ_APPROVAL":
        appr, _ = FinanceRequisitionApproval.objects.get_or_create(
            requisition_number=requisition_number, officer=request.user.profile
        )
        appr.remark = request.POST.get("remark", "")
        appr.approve_status = request.POST.get("status", "no")
        appr.funds_confirmed = request.POST.get("funds_confirmed", "off") == "on"
        appr.part_of_annual_plan = (
            request.POST.get("part_of_annual_plan", "off") == "on"
        )
        appr.annual_procurement_plan = request.POST.get("annual_procurement_plan", None)
        appr.save()
        approval.finance_requisition_approval = appr
        approval.save()

    url = reverse("detail_requisition_approval", args=(id,))
    return redirect(url)
