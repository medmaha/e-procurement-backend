from django.contrib import admin

# Register your models here.
from .models import GPPAUser


class GPPAUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(GPPAUser, GPPAUserAdmin)
