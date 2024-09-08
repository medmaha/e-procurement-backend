from django.contrib import admin
from django.http.request import HttpRequest
from . import models


class AccountAdmin(admin.ModelAdmin):
    sortable_by = ["is_active", "last_login"]


class GroupAdmin(admin.ModelAdmin):
    model = models.AuthGroup
    fields = [
        "name",
        (
            "group_id",
            "editable",
        ),
        "authored_by",
        "description",
    ]


# admin.site.register(models.AuthGroup)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.AuthGroup, GroupAdmin)
