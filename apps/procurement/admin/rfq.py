from django.contrib import admin

from ..models import (
    RFQ,
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    RFQEvaluation,
    RFQQuotationEvaluation,
)


class RFQAdmin(admin.ModelAdmin):
    model = RFQ

    sortable_by = []
    list_display = [
        "title",
        "officer",
        "open_status",
        "approval_status",
        "published",
        "last_modified",
    ]


admin.site.register(RFQ, RFQAdmin)
