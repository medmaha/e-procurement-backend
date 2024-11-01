from django.contrib import admin
from ..models import Requisition, RequisitionItem


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    pass


@admin.register(RequisitionItem)
class RequisitionItemAdmin(admin.ModelAdmin):
    pass
