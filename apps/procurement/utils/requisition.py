from datetime import date
from django.http import HttpRequest

from apps.accounts.models import Account

from ..models.requisition import generateReqNumber


def populate_requisition_form(request: HttpRequest, form_data=None):
    user: Account = request.user  # type: ignore
    if request.method == "GET" and form_data:
        if form_data.fields.get("originating_officer"):
            form_data.fields["originating_officer"].widget.attrs.update(
                {"value": user.full_name}
            )
            form_data.fields["user_department"].widget.attrs.update(
                {
                    "value": user.profile.department.name
                    if user.profile and user.profile.department
                    else ""
                }
            )
    elif request.method == "POST":
        form_data = request.POST.copy()
        form_data.update(
            {
                "requisition_number": generateReqNumber(),
                "requisition_date": str(date.today()),
                "originating_officer": user.profile.department,
                "user_department": user.profile,
            }
        )
        form_data.update(
            {"officer_id": user.profile.id, "department_id": user.profile.department.id}
        )
    else:
        form_data = {}
    return form_data
