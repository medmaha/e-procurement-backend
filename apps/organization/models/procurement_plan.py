import decimal
from django.db import models

from apps.core.utilities.text_choices import (
    ProcurementMethodChoices,
    MeasurementUnitChoices,
)
from apps.organization.models.staff import Staff
from apps.gppa.models import GPPAUser
from APP_COMPANY import APP_CONSTANTS
from apps.accounts.models.account import Account


class Threshold(models.Model):
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    max_amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=100, default="")
    gppa_requirement = models.BooleanField(default=False)
    procurement_method = models.CharField(
        max_length=100,
        choices=ProcurementMethodChoices.choices,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Procurement Threshold"

    def __str__(self):
        return self.procurement_method

    @staticmethod
    def get_matching_threshold(value):
        "Query for finding the appropriate Threshold"
        return Threshold.objects.filter(
            models.Q(min_amount__lte=value) & models.Q(max_amount__gte=value)
        ).first()


class PlanItem(models.Model):
    """Procurement Plan Items"""

    description = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(blank=True, null=True)
    budget = models.DecimalField(decimal_places=2, max_digits=20)
    measurement_unit = models.CharField(
        max_length=255,
        choices=MeasurementUnitChoices.choices,
    )
    procurement_method = models.CharField(
        max_length=255,
        choices=ProcurementMethodChoices.choices,
        default="",
        blank=True,
    )
    quarter_1_budget = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, default=decimal.Decimal(0)
    )
    quarter_2_budget = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, default=decimal.Decimal(0)
    )
    quarter_3_budget = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, default=decimal.Decimal(0)
    )
    quarter_4_budget = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, default=decimal.Decimal(0)
    )

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        matching_threshold = Threshold.objects.filter(
            min_amount__lte=self.budget, max_amount__gte=self.budget
        ).first()
        if matching_threshold:
            self.procurement_method = matching_threshold.procurement_method
            return super().save(*args, **kwargs)
        raise NotImplementedError("Not implemented yet")

    class Meta:
        ordering = ["-last_modified"]


class DepartmentProcurementPlan(models.Model):
    """
    The Department procurement plan, an essential component of the E-Procurement system
    """

    department = models.ForeignKey(
        "Department", null=True, blank=True, default=None, on_delete=models.CASCADE
    )
    description = models.TextField(
        max_length=100,
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(PlanItem, related_name="plan")

    def __str__(self) -> str:
        return "%s" % (self.department.name if self.department else "No department")

    class Meta:
        ordering = ["-last_modified"]


class AnnualPlan(models.Model):
    """
    The Annual procurement plan, the key component of the E-Procurement system
    """

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=750, null=True, blank=True)

    department_plans = models.ManyToManyField(
        DepartmentProcurementPlan, blank=True, related_name="annual_plan"
    )

    year_start = models.DateField(blank=True)
    renewed_year = models.DateField(blank=True, null=True)

    officer = models.ForeignKey(
        Staff,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    org_approved = models.BooleanField(
        default=False, help_text="Has the organization approved this plan?"
    )
    gppa_approved = models.BooleanField(
        default=False, help_text="Has GPPA approved this plan?"
    )
    is_operational = models.BooleanField(
        default=False, help_text="Is the plan operational?"
    )
    is_current_plan = models.BooleanField(
        default=False, help_text="Is the plan this valid for operations?"
    )

    latest_approval_request_date = models.DateTimeField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        if self.renewed_year:
            return "Year %s-%s" % (self.year_start.year, self.renewed_year.year)
        return "Year %s" % (self.year_start.year)

    @classmethod
    def get_current_plan(cls):
        return cls.objects.filter(is_current_plan=True).first()

    @classmethod
    def has_approvers(cls):
        group_names = [
            APP_CONSTANTS["GROUPS"]["Annual Procurement Approver"]["name"],
            APP_CONSTANTS["GROUPS"]["Annual Procurement Approver GPPA"]["name"],
        ]
        return Account.objects.filter(
            groups__name__in=group_names, is_active=True
        ).exists()

    @classmethod
    def get_plan_by_year(cls, year: str | None):
        "* Tries to get the annual plan based on provided year or else returns the current plan"
        plan = None
        print("Plan", plan)
        if not year:
            plan = cls.get_current_plan()
        else:
            try:
                int(year)
                plan = cls.objects.filter(year_start__year__lte=year).first()
                print("PlanB", plan)
            except Exception as e:
                print(e)
                plan = cls.get_current_plan()
                print("PlanC", plan)
        if not plan:
            plan = cls.objects.first()
            print("PlanD", plan)
        return plan

    @property
    def approvable(self):
        "Checks if the plan is apposable"
        if not self.has_approvers():
            return False
        test_0 = not self.latest_approval_request_date
        test_1 = (self.org_approved is None and self.gppa_approved is None) == True
        test_2 = (self.org_approved and self.gppa_approved is None) == True
        test_3 = (self.gppa_approved and self.org_approved is None) == True
        return test_0 or test_1 or test_2 or test_3

    def send_approval_emails(self, level):
        "A helper attribute to send the approval email"
        print("<====== Sending approval emails ======>")

    class Meta:
        verbose_name = "Annual Plan"
        ordering = ["-year_start", "-created_date", "-last_modified"]

    @property
    def items(self):
        return PlanItem.objects.filter(plan__in=self.department_plans.all())

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = "Annual Procurement Plan - Year %s" % self.year_start.year
        super().save(*args, **kwargs)

    def __str__(self):
        if not self.renewed_year:
            return f"Year {self.year_start.year}"
        if self.year_start.year == self.renewed_year.year:
            return f"Year {self.year_start.year}"
        return f"{self.year_start.year}/{self.renewed_year.year}"


class AnnualPlanApproval(models.Model):
    """* An approval record for annual procurement plan"""

    officer = models.ForeignKey(
        Staff,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    annual_plan = models.ForeignKey(
        AnnualPlan, on_delete=models.CASCADE, related_name="approval_record"
    )
    approved = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True, default="")

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.annual_plan)

    class Meta:
        verbose_name = "Annual Plan Approval"
        verbose_name_plural = "Annual Plan Approval"


class AnnualPlanApprovalGPPA(models.Model):
    """* An approval record made by GPPA, for annual procurement plan"""

    officer = models.ForeignKey(
        GPPAUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    annual_plan = models.ForeignKey(
        AnnualPlan, on_delete=models.CASCADE, related_name="gppa_approval_record"
    )
    approved = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True, default="")

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.annual_plan)

    class Meta:
        verbose_name = "Annual Plan Approval - GPPA"
        verbose_name_plural = "Annual Plan Approval - GPPA"
