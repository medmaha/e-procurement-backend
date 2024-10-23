from django.contrib import admin
from ..models.requisition_approval_workflow import (
    ApprovalAction,
    ApprovalMatrix,
    ApprovalStep,
    ApprovalWorkflow,
    Delegation,
)


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    pass


@admin.register(ApprovalMatrix)
class ApprovalMatrixAdmin(admin.ModelAdmin):
    pass


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    pass


@admin.register(ApprovalAction)
class ApprovalActionAdmin(admin.ModelAdmin):
    pass


@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    pass
