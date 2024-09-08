from django.contrib import admin

from .. import models


class StaffAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Staff, StaffAdmin)
