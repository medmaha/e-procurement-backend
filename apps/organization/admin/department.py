from django.contrib import admin
from .. import models


class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "department_head",
    ]


admin.site.register(models.Department, DepartmentAdmin)
