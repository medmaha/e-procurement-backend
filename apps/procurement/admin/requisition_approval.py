from django.contrib import admin
from ..models import RequisitionApproval


class RequisitionApprovalAdmin(admin.ModelAdmin):
    model = RequisitionApproval
