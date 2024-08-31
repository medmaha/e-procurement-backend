from django.contrib import admin

from ..models import (
    RFQ,
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    RFQEvaluation,
    RFQQuotationEvaluation,
)


admin.site.register(UnitRequisitionApproval)
admin.site.register(DepartmentRequisitionApproval)
admin.site.register(RFQEvaluation)
admin.site.register(RFQQuotationEvaluation)


class RFQAdmin(admin.ModelAdmin):
    model = RFQ

    search_fields = [
        "unique_id",
    ]
    sortable_by = []

    def get_list_display(self, request, obj=None):
        _list = [
            "title",
            "officer",
            "open_status",
            "approval_status",
            "published",
            "last_modified",
        ]

        return _list
