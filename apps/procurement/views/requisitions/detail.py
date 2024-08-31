from datetime import date
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required
from apps.core.decorators.permissions import staff_view

from apps.procurement.forms import RequisitionDetailForm
from apps.procurement.models import Requisition, RequisitionApproval


@login_required
@staff_view
def requisitions_detail(request, id):
    error_message = None
    success_message = None
    profile = request.user.profile

    requisition = get_object_or_404(Requisition, requisition_number=id)

    if request.method == "POST":
        data = request.POST.copy()
        data.update({"staff": str(profile.pk)})
        form = RequisitionDetailForm(data=data, instance=requisition)
        if form.is_valid():
            form.save()
            form.instance.staff = request.user.profile
            return redirect("/")

        else:
            error_message = "invalid request"

    form = RequisitionDetailForm(instance=requisition)
    approval = RequisitionApproval.objects.filter(
        requisition=requisition,
    )

    is_pending = approval.filter(
        unit_approval__isnull=True,
        department_approval__isnull=True,
        procurement_requisition_approval__isnull=True,
        finance_requisition_approval__isnull=True,
    ).exists()

    context = {
        "form": form,
        "requisition": requisition,
        "approval": approval.first(),
        "is_pending": is_pending,
        "error_message": error_message,
        "success_message": success_message,
    }

    template_url = "procurement/requisitions/detail.html"

    if is_pending:
        template_url = "procurement/requisitions/update.html"

    return render(
        request,
        template_url,
        context=context,
        status=200 if not error_message else 400,
    )
