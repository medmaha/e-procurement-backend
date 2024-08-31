from django import forms
from django.contrib import admin

from apps.procurement.models.requisition_approvals import ProcurementRequisitionApproval


class Form(forms.ModelForm):
    class Meta:
        model = ProcurementRequisitionApproval
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remark"].widget.attrs["rows"] = 2
        self.fields["remark"].widget.attrs["required"] = False


class ProcurementRequisitionAdmin(admin.StackedInline):
    extra = 0
    form = Form
    max_num = 1
    min_num = 0
    model = ProcurementRequisitionApproval


# admin.site.register(ProcurementRequisitionApproval)
