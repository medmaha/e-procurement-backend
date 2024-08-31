from datetime import date
from django.http import HttpRequest

from apps.accounts.models import Account

from ..models.rfq import generateRFQNumber


def populate_rfq_form(request: HttpRequest, form_data=None):
    user: Account = request.user  # type: ignore
    if not user.profile:
        return form_data
    if request.method == "GET" and form_data:
        if "originating_officer" in form_data.fields:
            form_data.fields["originating_officer"].widget.attrs.update(
                {"value": user.profile.employee_id}
            )
        if "officer_department" in form_data.fields:
            form_data.fields["officer_department"].widget.attrs.update(
                {"value": user.profile.department or ""}
            )

        if "approval_officer" in form_data.fields:
            form_data.fields["approval_officer"].widget.attrs.update({"type": "hidden"})
        if "approval_status" in form_data.fields:
            form_data.fields["approval_status"].widget.attrs.update({"type": "hidden"})

    elif request.method == "POST":
        form_data = request.POST.copy()
        form_data.update(
            {
                "rfq_number": generateRFQNumber(),
                "rfq_date": str(date.today()),
                "employee_id": user.profile.employee_id,
                "department_id": user.profile.department.pk,
            }
        )
        # form_data.update(
        #     {"officer_id": user.profile.id, "department_id": user.profile.department.id}
        # )
    else:
        form_data = {}
    return form_data
