from typing import Any
from django.db import models
from django.utils import timezone


from django.db.models import Manager
from apps.organization.models import Staff
from apps.procurement.models.requisition import Requisition
from apps.core.utilities.text_choices import (
    ApprovalChoices,
    MeasurementUnitChoices,
    ProcurementMethodChoices,
    RFQLevelChoices,
)
from apps.vendors.models import Vendor
from apps.core.utilities.generators import generate_unique_id


class RFQManager(Manager):

    def filter(self, *args: Any, **kwargs: Any):
        filter_results = super().filter(*args, **kwargs)

        # get all rfq has reaches evaluation level but not updated yet
        # TODO  need to change this logic
        (
            filter_results.select_related()
            .filter(required_date__lte=timezone.now(), open_status=True)
            .update(open_status=False, level=RFQLevelChoices.EVALUATION_LEVEL)
        )

        return filter_results


class RFQ(models.Model):
    objects = RFQManager()
    officer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="rfq_officer",
        help_text="Authorizes this instance",
    )

    requisition = models.ForeignKey(
        Requisition,
        on_delete=models.SET_NULL,
        null=True,
        related_name="rfq",
        help_text="The requisition record of which this RFQ is initiated for",
    )
    title = models.CharField(
        blank=True,
        max_length=255,
        default="Form 101 - Requests For Quotation",
        help_text="The title helps with organizing and identifying your rfq's ",
    )

    description = models.TextField(blank=True, default="")
    approval_status = models.CharField(
        max_length=100, choices=ApprovalChoices.choices, default="pending"
    )
    open_status = models.BooleanField(default=False)
    level = models.CharField(
        max_length=50,
        choices=RFQLevelChoices.choices,
        default=RFQLevelChoices.APPROVAL_LEVEL,
    )
    required_date = models.DateTimeField()

    suppliers = models.ManyToManyField(Vendor, blank=True, related_name="rfq_requests")
    terms_and_conditions = models.TextField(default="")
    published = models.BooleanField(
        default=False, blank=True, help_text="Publish this rfq to all suppliers"
    )
    auto_publish = models.BooleanField(
        default=False,
        help_text="Auto publish the RFQ when its approved",
    )

    opened_by = models.ManyToManyField(
        Staff,
        help_text="List of staffs that opens this procurement",
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def unique_id(self):
        return generate_unique_id("RFQ", self.pk, 5)

    @property
    def deadline(self):
        return self.required_date

    @property
    def requires_gppa_approval(self):
        requisition_approval = self.requisition.approval_record  # type: ignore
        return (
            requisition_approval.procurement_method.lower()
            == ProcurementMethodChoices.REQUEST_FOR_QUOTATION_2.value.lower()
        )

    class Meta:
        get_latest_by = "-created_date"
        ordering = ("-created_date",)

    def __str__(self):
        return self.unique_id

    @property
    def items(self):
        return RFQItem.objects.filter(rfq=self)


class RFQItem(models.Model):
    rfq = models.ForeignKey(
        "RFQ",
        on_delete=models.CASCADE,
        related_name="rfq_items_set",
        null=True,
        blank=True,
    )
    item_description = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.IntegerField(default=1)
    measurement_unit = models.CharField(
        max_length=255, choices=MeasurementUnitChoices.choices
    )
    remark = models.CharField(max_length=255, null=True, blank=True)
    eval_criteria = models.CharField(max_length=255, blank=True, default="")
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RFQ Item"
