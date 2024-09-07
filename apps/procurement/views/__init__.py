from datetime import date, timedelta
import datetime
from django.http import HttpRequest
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.organization.models import Staff
from apps.procurement.views.requisitions.create import requisitions_create
from apps.procurement.views.requisitions.detail import requisitions_detail

from ..forms import RFQForm, RFQItemsForm, RequisitionForm

from ..models import Requisition


@login_required
def procurement_view(request):
    context = {
        "active_tab": "procurement",
        "heading": "Select a Procurement method",
        "heading_desc": "Choose the most suitable procurement approach for your needs.",
    }
    return render(request, "procurements/index.html", context=context)


@login_required
def procurement_method(request: HttpRequest):
    context = {
        "error_message": "",
        "active_tab": "procurement",
        "heading": "Select a Procurement method",
        "heading_desc": "Choose the most suitable procurement approach for your needs.",
    }

    if request.method != "POST":
        context["error_message"] = "[Error] Method not supported"
        return render(request, "procurements/index.html", context=context, status=405)

    p_method = request.POST.get("procurement_method")

    if not p_method:
        context["error_message"] = "[Error] Procurement method is required"
        return render(request, "procurements/index.html", context=context, status=400)

    if not p_method in ["tender", "rfq", "ss"]:
        context["error_message"] = "[Error] Procurement method is required"
        return render(request, "procurements/index.html", context=context, status=400)

    if p_method == "rfq":
        return redirect(reverse("rfq"))
    if p_method == "tender":
        return redirect(reverse("tender"))
    return redirect(reverse("single_source"))


def requisitions_accepted(request: HttpRequest):
    staff_account = request.user.profile  # type: ignore
    requisitions = Requisition.objects.filter(
        originating_officer=staff_account, requisition_status="accepted"
    )

    context = {
        "requisitions": requisitions,
    }
    return render(request, "procurement/requisitions/accepted.html", context=context)


def requisitions_rejected(request: HttpRequest):
    staff_account = request.user.profile  # type: ignore
    requisitions = Requisition.objects.filter(
        originating_officer=staff_account, requisition_status="rejected"
    )

    context = {
        "requisitions": requisitions,
    }
    return render(request, "procurement/requisitions/rejected.html", context=context)


@login_required
def requisitions_pending(request: HttpRequest):
    staff_account = request.user.profile  # type: ignore
    requisitions = Requisition.objects.filter(
        originating_officer=staff_account, requisition_status="pending"
    )

    context = {
        "requisitions": requisitions,
    }
    return render(request, "procurement/requisitions/pending.html", context=context)


def requisitions_all(request: HttpRequest):
    staff_account = request.user.profile  # type: ignore
    requisitions = Requisition.objects.filter(originating_officer=staff_account)

    context = {
        "requisitions": requisitions,
    }
    return render(request, "procurement/requisitions/view_all.html", context=context)


def rfq(request: HttpRequest):
    rfq_form = RFQForm(request.POST or None)
    rfq_items_form = RFQItemsForm(request.POST or None)
    context = {"rfq_form": rfq_form, "rfq_items_form": rfq_items_form}
    return render(request, "procurements/rfq.html", context=context)


def rfq_detail(request: HttpRequest):
    rfq_form = RFQForm(request.POST or None)
    rfq_items_form = RFQItemsForm(request.POST or None)
    context = {"rfq_form": rfq_form, "rfq_items_form": rfq_items_form}
    return render(request, "procurements/rfq.html", context=context)


def tender(request):
    context = {
        "error_message": "",
        "active_tab": "procurement",
        "heading": "Select a Procurement method",
        "heading_desc": "Choose the most suitable procurement approach for your needs.",
    }
    return render(request, "procurements/tender.html", context=context)


def single_source(request):
    context = {
        "error_message": "",
        "active_tab": "procurement",
        "heading": "Select a Procurement method",
        "heading_desc": "Choose the most suitable procurement approach for your needs.",
    }
    return render(request, "procurements/single-sourcing.html", context=context)
