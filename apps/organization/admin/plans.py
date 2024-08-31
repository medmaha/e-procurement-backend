from django.contrib import admin
from .. import models


class ProcurementPlanItemsAdmin(admin.ModelAdmin):
    pass


class PlanItemInline(admin.TabularInline):
    model = models.PlanItem
    extra = 2

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return super().get_extra(request, obj, **kwargs)


class DepartmentProcurementPlanAdmin(admin.ModelAdmin):
    pass


class ThresholdAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "procurement_method",
        "min_amount",
        "max_amount",
    ]

    sortable_by = [
        "min_amount",
        "max_amount",
    ]

    list_filter = [
        "procurement_method",
    ]


class AnnualPlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "title",
        "is_current_plan",
        "org_approved",
        "gppa_approved",
        "is_operational",
    ]


admin.site.register(models.DepartmentProcurementPlan, DepartmentProcurementPlanAdmin)
admin.site.register(models.Threshold, ThresholdAdmin)
admin.site.register(models.AnnualPlan, AnnualPlanAdmin)
