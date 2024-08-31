from django.contrib import admin
from django.http.request import HttpRequest
from . import models


class AccountAdmin(admin.ModelAdmin):
    sortable_by = ["is_active", "last_login"]

    fields = [
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "password",
        "first_name",
        "middle_name",
        "last_name",
        "groups",
        "last_login",
    ]
    readonly_fields = ["last_login"]

    def get_list_display(self, request: HttpRequest):
        list_display = [
            "full_name",
            "first_name",
            "last_name",
            "profile_type",
            "is_active",
            "__groups__",
            "last_login",
        ]
        return list_display


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
