from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404, redirect

from apps.vendors.forms import QuoteForm
from apps.procurement.models.rfq import RFQ


@login_required
def quotation_list(request):
    profile = request.user.profile
    quotations = RFQ.objects.filter(vendor=profile)
    context = {"quotations": quotations, "active_tab": "quotations"}
    return render(request, "vendors/quotation_list.html", context=context)


@login_required
def quotation_detail(request, id):
    error_msg = None
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "quote":
            response = redirect(reverse("quotation_accept", args=(id,)))
            return response
        elif action == "reject":
            response = redirect(reverse("quotation_reject", args=(id,)))
            return response
        else:
            error_msg = "Invalid action '%s' for" % action

    quotation = get_object_or_404(RFQ, unique_id=id)
    context = {
        "quotation": quotation,
        "active_tab": "quotations",
        "error_message": error_msg,
    }
    return render(request, "vendors/quotation_detail.html", context=context)


@login_required
def quotation_accept(request, id):
    quotation = get_object_or_404(RFQ, unique_id=id)
    form = QuoteForm()

    context = {"quotation": quotation, "active_tab": "quotations", "form": form}
    if request.method == "POST":
        data = request.POST.copy()
        context["success_message"] = (
            "We've received you quote fot quotation %s %s %s your request is being processed"
            % ('"', quotation.unique_id, '"')
        )
    return render(request, "vendors/quotation_accept.html", context=context)


@login_required
def quotation_reject(request, id):
    quotation = get_object_or_404(RFQ, unique_id=id)
    context = {"quotation": quotation, "active_tab": "quotations"}

    if request.method == "POST":
        data = request.POST.copy()
        context["success_message"] = (
            "We've notice your rejection for quotation %s, your request is being processed"
            % quotation.unique_id
        )
    return render(request, "vendors/quotation_reject.html", context=context)
