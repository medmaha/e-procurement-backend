from django.urls import path, re_path, include
from django.http import HttpRequest, JsonResponse
from .views import index
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view()
@permission_classes([])
# @authentication_classes([])
def not_found(request: HttpRequest):
    import secrets

    data = {
        "status": 404,
        "message": "This route does not exists",
        "details": [
            "You've hit our server perfectly! perhaps you missed the url address",
        ],
        "request": {},
    }
    account = request.user
    if account.is_authenticated:
        profile_type, profile = request.user.get_profile()  # type: ignore
        data["request"]["Authenticated"] = True
        data["request"]["User"] = {
            "Account Type": profile_type,  # type: ignore
            "Full Name": account.full_name,  # type: ignore
        }
    else:
        data["request"]["Authenticated"] = False

    data["request"]["Origin"] = request.headers.get("sec-fetch-site") or "Unknown"
    data["request"]["HASH-KEY"] = secrets.token_hex(12)
    data["request"]["Client Agent"] = request.headers.get("User-Agent")

    return JsonResponse(data, status=404)


urlpatterns = [
    # path("", index, name="index"),
    path("api/company/", include("apps.app.api.urls")),
    path("api/account/", include("apps.accounts.api.urls")),
    # path(r"api/organization/", include("apps.organization.api.urls")),
    # path(r"api/procurement/", include("apps.procurement.api.urls")),
    # path(r"api/vendors/", include("apps.vendors.api.urls")),
    # re_path(r"^api/", not_found, name="not_found"),
]
