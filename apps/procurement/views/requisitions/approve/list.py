from django.shortcuts import render
from apps.core.decorators.permissions import staff_view
from django.contrib.auth.decorators import login_required
from apps.procurement.models.requisition_approval import RequisitionApproval


@login_required
@staff_view
def approve_list(request):
    requisition_approvals = RequisitionApproval.objects.filter()

    user_groups = request.permissions

    context = {
        "active_tab": "home",
        "requisition_approvals": requisition_approvals,
        "groups": user_groups,
    }
    return render(
        request, "procurement/requisitions/approve/index.html", context=context
    )
