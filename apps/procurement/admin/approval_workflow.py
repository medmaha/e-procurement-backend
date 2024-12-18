from django.contrib import admin
from ..models import (
    ApprovalAction,
    ApprovalMatrix,
    ApprovalStep,
    ApprovalWorkflow,
    Delegation,
    WorkflowStep,
)


@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ["workflow", "step", "order", "condition_type", "created_date"]


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    pass


@admin.register(ApprovalMatrix)
class ApprovalMatrixAdmin(admin.ModelAdmin):
    pass


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "order",
        "role",
        "approver",
        "is_final",
        "time_limit",
        "last_modified",
    ]


@admin.register(ApprovalAction)
class ApprovalActionAdmin(admin.ModelAdmin):
    pass


@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    pass
