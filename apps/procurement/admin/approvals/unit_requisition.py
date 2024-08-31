from django import forms
from django.contrib import admin

from apps.procurement.models.requisition_approvals import UnitRequisitionApproval


class Form(forms.ModelForm):
    class Meta:
        model = UnitRequisitionApproval
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "remark" in self.fields:
            self.fields["remark"].widget.attrs["rows"] = 2
            self.fields["remark"].widget.attrs["required"] = False


class UnitApprovalRequisitionAdmin(admin.StackedInline):
    extra = 0
    form = Form
    max_num = 1
    min_num = 0
    model = UnitRequisitionApproval

    readonly_fields = ["officer", "created_date", "last_modified"]

    def get_fields(self, request, obj, *args, **kwargs):
        fields = ["approve", "remark"]
        if obj.unit_approval(False):
            fields.insert(0, "officer")
            if obj.finance_approval(False):
                fields = fields + ["created_date", "last_modified"]
        return fields

    def has_view_permission(self, request, obj=None):
        if obj:
            return True
        return super().has_view_permission(request, obj)


# admin.site.register(UnitRequisitionApproval)
