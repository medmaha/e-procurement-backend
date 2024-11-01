from django.db import models

from apps.organization.models import Staff
from apps.core.utilities.text_choices import (
    MeasurementUnitChoices,
    ApprovalChoices,
    PRStatusChoices,
)
from apps.organization.models.department import Department


def upload_to(instance, filename: str):
    "Uploads the statement of requirement on a specified location"
    _path = "procurement/requisitions/statements_files/%s/%s" % (
        instance.officer.pk,
        filename,
    )
    return _path


class RequisitionItem(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    measurement_unit = models.CharField(
        max_length=100, choices=MeasurementUnitChoices.choices
    )
    unit_cost = models.FloatField(null=True, default=float(4250.00))
    total_cost = models.FloatField(null=True, default=float(4250.00))
    remark = models.CharField(null=True, blank=True, max_length=100)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.unit_cost:
            self.total_cost = self.unit_cost * self.quantity
        super(RequisitionItem, self).save(*args, **kwargs)


class Requisition(models.Model):
    items = models.ManyToManyField(RequisitionItem)
    request_type = models.CharField(max_length=100, default="Work")
    statement_of_requirements = models.FileField(
        upload_to=upload_to,
        null=True,
        blank=True,
        help_text="Max 10MB, filetypes pdf, txt, docx",
    )
    approval_status = models.CharField(
        max_length=255,
        blank=True,
        default=ApprovalChoices.PENDING,
        choices=ApprovalChoices.choices,
    )
    pr_status = models.CharField(
        max_length=255,
        blank=True,
        default=PRStatusChoices.PENDING,
        choices=PRStatusChoices.choices,
    )
    officer = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        help_text="Authorizes this instance",
    )

    officer_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The department that the officer belongs to at the time of creation",
    )

    current_approval_step = models.ForeignKey(
        "WorkflowStep", null=True, blank=True, on_delete=models.SET_NULL
    )

    remarks = models.TextField(null=True, blank=True, default="")
    date_required = models.DateTimeField(auto_now_add=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    @property
    def total_price(self):
        return sum([item.total_cost for item in self.items.filter()])

    def get_approval_matrix(self):
        from apps.procurement.models.pr_approval_utils import get_matrix_for_requisition

        return get_matrix_for_requisition(self)
