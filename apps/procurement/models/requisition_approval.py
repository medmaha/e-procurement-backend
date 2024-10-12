from django.db import models

from apps.procurement.models.requisition import Requisition
from apps.core.utilities.text_choices import (
    ApprovalChoices,
    ProcurementMethodChoices,
)
from apps.core.utilities.generators import generate_unique_id
from apps.accounts.models.account import Account

from .requisition_approvals import (
    UnitRequisitionApproval,
    DepartmentRequisitionApproval,
    ProcurementRequisitionApproval,
    FinanceRequisitionApproval,
)


def upload_to(instance, filename: str):
    _path = "procurement/"
    if instance.hasattr("statement_of_requirements"):
        _path += instance.originating_officer.email + "/statements/" + filename
    return _path


class RequisitionApproval(models.Model):
    requisition = models.OneToOneField(
        Requisition,
        on_delete=models.CASCADE,
        help_text="The requisition that is being approved",
        related_name="approval_record",
    )
    unit_approval = models.OneToOneField(
        UnitRequisitionApproval,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="approval",
    )
    department_approval = models.OneToOneField(
        DepartmentRequisitionApproval,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="approval",
    )
    procurement_approval = models.OneToOneField(
        ProcurementRequisitionApproval,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="approval",
    )
    finance_approval = models.OneToOneField(
        FinanceRequisitionApproval,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="approval",
    )
    procurement_method = models.CharField(
        choices=ProcurementMethodChoices.choices,
        default=ProcurementMethodChoices.SINGLE_SOURCING,
        max_length=255,
    )
    status = models.CharField(
        max_length=255,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING,
        null=False,
    )
    editable = models.BooleanField(default=True, blank=True, null=False)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        ordering = ["-id"]

    @property
    def unique_id(self):
        return generate_unique_id("APR", self.pk)

    def __str__(self):
        return str(self.unique_id)

    def has_approve_perm(self, user: Account):

        if self.status != ApprovalChoices.PENDING:
            return False

        if not self.unit_approval:
            return user.has_perm(
                f"{UnitRequisitionApproval._meta.app_label}.add_{UnitRequisitionApproval._meta.model_name}"
            )
        if not self.department_approval:
            return user.has_perm(
                f"{DepartmentRequisitionApproval._meta.app_label}.add_{DepartmentRequisitionApproval._meta.model_name}"
            )
        if not self.finance_approval:
            return user.has_perm(
                f"{FinanceRequisitionApproval._meta.app_label}.add_{FinanceRequisitionApproval._meta.model_name}"
            )
        if not self.procurement_approval:
            return user.has_perm(
                f"{ProcurementRequisitionApproval._meta.app_label}.add_{ProcurementRequisitionApproval._meta.model_name}"
            )
        return False

    def get_stage(self):
        if self.status == ApprovalChoices.PENDING.value:
            if not self.unit_approval:
                return ("Unit", self.unit_approval)
            if not self.department_approval:
                return ("Department", self.department_approval)
            if not self.finance_approval:
                return ("Finance", self.finance_approval)
            if not self.procurement_approval:
                return ("Procurement", self.procurement_approval)
        return ("", None)

    @property
    def stage(self) -> str:
        return self.get_stage()[0]

    @property
    def stage_model(self):
        return self.get_stage()[1]
