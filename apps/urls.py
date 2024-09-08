from django.urls import path, re_path, include
from django.http import JsonResponse

from .views import index, NotFoundView, APINotFoundView


def test(_):
    return JsonResponse(
        {
            "status": 200,
            "message": "Web server is up and running",
        }
    )


urlpatterns = [
    path("", index, name="index"),
    path("test/", test, name="test"),
    path("api/auth/", include("apps.accounts.api.auth_urls")),
    path("api/users/", include("apps.accounts.api.user_urls")),
    path("api/org/", include("apps.organization.api.urls")),
    # path(r"api/procurement/", include("apps.procurement.api.urls")),
    # path(r"api/vendors/", include("apps.vendors.api.urls")),
    re_path(r"^api/.*/$", APINotFoundView.as_view()),
    re_path(r"^.*/$", NotFoundView.as_view()),
]
