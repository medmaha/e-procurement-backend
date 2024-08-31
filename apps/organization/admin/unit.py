from django.contrib import admin
from django.http.request import HttpRequest
from django.contrib.auth.models import Permission

from .. import models


class UnitsAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "department",
        "description",
    ]


admin.site.register(models.Unit, UnitsAdmin)
