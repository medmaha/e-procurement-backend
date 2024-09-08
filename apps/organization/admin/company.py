from django.contrib import admin
from .. import models


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Company, CompanyAdmin)
