from django.contrib import admin
from django.urls import include, path, re_path

from django.conf import settings
from django.conf.urls.static import static

from APP_COMPANY import APP_COMPANY

from .admin import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.urls")),
    re_path(r"^", include("apps.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = APP_COMPANY.get("name", "") + " | E-Procurement"
admin.site.site_title = APP_COMPANY.get("name", "") + " - Procurement Portal"
admin.site.site_header = admin.site.index_title
