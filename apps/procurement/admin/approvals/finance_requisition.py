from django import forms
from django.contrib import admin

from apps.procurement.models.requisition_approvals import FinanceRequisitionApproval


class Form(forms.ModelForm):
    class Meta:
        model = FinanceRequisitionApproval
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remark"].widget.attrs["rows"] = 2
        self.fields["remark"].widget.attrs["required"] = False


# admin.site.register(FinanceRequisitionApproval)


class FinanceRequisitionAdmin(admin.StackedInline):
    extra = 0
    form = Form
    max_num = 1
    min_num = 0
    model = FinanceRequisitionApproval
    readonly_fields = ["officer", "created_date", "last_modified"]

    def get_fields(self, request, obj, *args, **kwargs):
        fields = [
            "approve",
            "funds_confirmed",
            "part_of_annual_plan",
            "annual_procurement_plan",
            "remark",
        ]
        if obj.finance_approval(False):
            fields.insert(0, "officer")
            if obj.finance_approval(False):
                fields = fields + ["created_date", "last_modified"]
        return fields
