from datetime import date
import secrets
from django.http import HttpRequest

from apps.accounts.models import Account


def populate_requisition_approval_form(request: HttpRequest, form_data):
    user: Account = request.user  # type: ignore
    if request.method == "GET":
        if "approval_officer" in form_data.fields:
            form_data.fields["approval_officer"].widget.attrs.update(
                {"value": str(user.profile) if user.profile else None}
            )
        if "approval_officer_department" in form_data.fields:
            form_data.fields["approval_officer_department"].widget.attrs.update(
                {
                    "value": (
                        str(user.profile.department)
                        if (user.profile and user.profile.department)
                        else None
                    )
                }
            )

    elif request.method == "POST":
        form_data = request.POST.copy()
        form_data.update(
            {
                "requisition_approval_number": secrets.token_hex(12),
                "approval_date": str(date.today()),
                "approval_officer_department": user.profile.department,
                "approval_officer": user.profile,
            }
        )
        form_data.update(
            {"officer_id": user.profile.id, "department_id": user.profile.department.id}
        )
    else:
        form_data = {}
    return form_data
