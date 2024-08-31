from django.http import HttpRequest
from APP_COMPANY import APP_COMPANY


CURRENCY = "D"


def app_company(request: HttpRequest):
    permissions = request.permissions  # type: ignore

    return {
        "company": APP_COMPANY,
        "CURRENCY": CURRENCY,
        "auth_permissions": permissions,
    }
