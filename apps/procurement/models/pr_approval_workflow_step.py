from django.db import models
from django.utils import timezone
from decimal import Decimal

from apps.organization.models import Staff
from apps.procurement.models.requisition import Requisition
from apps.procurement.models.pr_approval_step import ApprovalStep
from apps.procurement.models.pr_approval_workflow import ApprovalWorkflow


class WorkflowStep(models.Model):
    """
    Model representing the connection between ApprovalWorkflow and ApprovalStep.
    """

    class ConditionType(models.TextChoices):
        AMOUNT_GREATER_THAN = "amount_gt", "Amount greater than"
        AMOUNT_LESS_THAN = "amount_lt", "Amount less than"
        DEPARTMENT_EQUALS = "dept_eq", "Department equals"
        UNIT_EQUALS = "unit_eq", "Unit equals"
        ALWAYS = "always", "Always execute"
        # New conditions
        ITEM_COUNT_GREATER_THAN = "item_count_gt", "Item count greater than"
        REQUISITION_TYPE_EQUALS = "req_type_eq", "Requisition type equals"
        DAYS_SINCE_SUBMISSION = "days_since_sub", "Days since submission"

    author = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE)
    step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    order = models.IntegerField()
    condition_type = models.CharField(
        max_length=20, choices=ConditionType.choices, default=ConditionType.ALWAYS
    )
    condition_value = models.CharField(max_length=255, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def check_condition(self, requisition: Requisition) -> bool:
        """
        Check if the condition for this step is met.
        """
        try:
            if self.condition_type == WorkflowStep.ConditionType.ALWAYS:
                return True
            elif self.condition_type == WorkflowStep.ConditionType.AMOUNT_GREATER_THAN:
                return requisition.total_price > Decimal(self.condition_value or "")
            elif self.condition_type == WorkflowStep.ConditionType.AMOUNT_LESS_THAN:
                return requisition.total_price < Decimal(self.condition_value or "")
            elif self.condition_type == WorkflowStep.ConditionType.DEPARTMENT_EQUALS:
                return requisition.officer_department is not None and (
                    str(requisition.officer_department.pk) == self.condition_value
                )
            elif self.condition_type == WorkflowStep.ConditionType.UNIT_EQUALS:
                return str(requisition.officer.unit.pk) == self.condition_value
            # New condition checks
            elif (
                self.condition_type
                == WorkflowStep.ConditionType.ITEM_COUNT_GREATER_THAN
            ):
                return requisition.items.count() > int(self.condition_value or "")
            elif (
                self.condition_type
                == WorkflowStep.ConditionType.REQUISITION_TYPE_EQUALS
            ):
                return requisition.requisition_type == self.condition_value  # type: ignore
            elif (
                self.condition_type == WorkflowStep.ConditionType.DAYS_SINCE_SUBMISSION
            ):
                days_since = (timezone.now() - requisition.submission_date).days  # type: ignore
                return days_since > int(self.condition_value or "")
            return False
        except Exception as e:
            return False

    class Meta:
        ordering = ["order"]
        unique_together = ["workflow", "order"]

    def __str__(self):
        return f"{self.workflow.name} - Step {self.order}: {self.step.name}"
