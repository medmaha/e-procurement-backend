from django.contrib import admin

from apps.procurement.models.rfq_approval import RFQApproval, RFQApprovalGPPA

admin.site.register(RFQApprovalGPPA)
admin.site.register(RFQApproval)


class RFQApprovalAdmin(admin.StackedInline):
    extra = 0
    max_num = 1
    min_num = 0
    model = RFQApproval
    readonly_fields = ["officer", "created_date", "last_modified"]

    def get_fields(self, request, obj, *args, **kwargs):
        fields = ["approve", "remark"]
        try:
            if obj and obj.approval_record:
                # fields.insert(0, "officer")
                fields = fields + [("created_date", "last_modified")]
        except:
            pass
        return fields

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:  # type: ignore
            return True
        if obj:
            return False
        return True
