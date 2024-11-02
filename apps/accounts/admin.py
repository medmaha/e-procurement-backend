from collections.abc import Sequence
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http.request import HttpRequest
from . import models


class AccountAdmin(admin.ModelAdmin):
    sortable_by = ["is_active", "last_login"]
    list_display: Sequence[str] = [
        "email",
        "full_name",
        "profile_type",
        "is_active",
        "__groups__",
        "last_login",
    ]


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
admin.site.register(Permission)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.AuthGroup, GroupAdmin)
