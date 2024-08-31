from django import forms
from django.contrib import admin

from apps.procurement.models.requisition_approvals import DepartmentRequisitionApproval


class Form(forms.ModelForm):
    class Meta:
        model = DepartmentRequisitionApproval
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remark"].widget.attrs["rows"] = 2
        self.fields["remark"].widget.attrs["required"] = False


# admin.site.register(DepartmentRequisitionApproval)


class DepartmentRequisitionAdmin(admin.StackedInline):
    form = Form
    extra = 0
    max_num = 1
    min_num = 0
    model = DepartmentRequisitionApproval
    readonly_fields = ["officer", "created_date", "last_modified"]

    def get_fields(self, request, obj, *args, **kwargs):
        fields = ["approve", "remark"]
        if obj:
            fields.insert(0, "officer")
            if obj.department_approval(False):
                fields = fields + ["created_date", "last_modified"]
        return fields
