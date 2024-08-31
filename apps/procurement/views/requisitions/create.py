from datetime import date
from django.http import HttpRequest
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from apps.core.decorators.permissions import create_requisition, staff_view
from apps.organization.models import Staff
from apps.procurement.models.requisition import generateReqNumber

from apps.procurement.forms import RequisitionForm


@login_required
@staff_view
@create_requisition
def requisitions_create(request):
    form = RequisitionForm()
    error_message = None
    success_message = None

    if request.method == "POST":
        data = request.POST.copy()

        unit_cost = data.get("estimated_unit_cost", 0)
        quantity = data.get("quantity", 0)
        total_cost = int(unit_cost) * int(quantity)
        requisition_date = date.today()

        data.update(
            {
                "estimated_total_cost": str(total_cost),
                "requisition_date": str(requisition_date),
                "requisition_status": "pending",
                "requisition_number": generateReqNumber(),
                "staff": str(request.user.profile.pk),
            }
        )
        form = RequisitionForm(data)
        if form.is_valid():
            form.save()
            form.instance.staff = request.user.profile
            return redirect("/")

        else:
            error_message = "invalid request"

    context = {
        "form": form,
        "form.errors": None,
        "error_message": error_message,
        "success_message": success_message,
    }
    return render(
        request,
        "procurement/requisitions/create.html",
        context=context,
        status=200 if not error_message else 400,
    )
