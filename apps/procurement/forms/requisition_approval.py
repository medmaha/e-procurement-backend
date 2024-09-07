from django import forms

from ..models import (
    RequisitionApproval,
)


from ..models import requisition_approvals


class RequisitionApprovalForm(forms.ModelForm):
    class Meta:
        model = RequisitionApproval
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if (
            "finance_requisition_approval" in self.fields
            and not self.instance.finance_requisition_approval
        ):
            self.fields["finance_requisition_approval"].queryset = (
                requisition_approvals.FinanceRequisitionApproval.objects.filter(
                    finance_req_approval_set__isnull=True
                )
            )
        if (
            "procurement_requisition_approval" in self.fields
            and not self.instance.procurement_requisition_approval
        ):
            self.fields["procurement_requisition_approval"].queryset = (
                requisition_approvals.ProcurementRequisitionApproval.objects.filter(
                    procurement_req_approval_set__isnull=True
                )
            )
        if (
            "department_approval" in self.fields
            and not self.instance.department_approval
        ):
            self.fields["department_approval"].queryset = (
                requisition_approvals.DepartmentRequisitionApproval.objects.filter(
                    department_req_approval_set__isnull=True
                )
            )
        if "unit_approval" in self.fields and not self.instance.unit_approval:
            self.fields["unit_approval"].queryset = (
                requisition_approvals.UnitRequisitionApproval.objects.filter(
                    unit_req_approval_set__isnull=True
                )
            )
