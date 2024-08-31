from django.contrib import admin

from .. import models


class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone",
        "job_title",
        "employee_id",
    ]
    save_as_continue = False
    readonly_fields = [
        "employee_id",
        "user_account",
    ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:  # type: ignore
            return True
        if obj and obj.user_account == request.user:
            return True
        return False


admin.site.register(models.Staff, StaffAdmin)
