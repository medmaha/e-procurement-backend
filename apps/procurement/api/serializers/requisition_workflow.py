from rest_framework import serializers


from apps.procurement.models.requisition_approval_workflow import (
    ApprovalWorkflow,
    WorkflowStep,
    ApprovalStep,
)


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = ("id", "name", "description", "created_date", "last_modified")

    def to_representation(self, instance: ApprovalWorkflow):
        data = super().to_representation(instance)

        if instance.author:
            data["officer"] = {
                "id": instance.author.pk,
                "name": instance.author.name,
            }

        workflow_id = self.context.get("workflow_id")

        if workflow_id:
            data["approval_steps"] = [
                {
                    "id": step.pk,
                    "order": step.order,
                    "name": step.name,
                    "role": step.role,
                    "description": step.description,
                    "department": (
                        {
                            "id": step.department.pk,
                            "name": step.department.name,
                        }
                        if step.department
                        else None
                    ),
                    "officer": (
                        {
                            "id": step.approver.pk,
                            "name": step.approver.name,
                        }
                        if step.approver
                        else None
                    ),
                    "remarks": step.remarks,
                    "is_final": step.is_final,
                    "is_optional": step.is_optional,
                    "time_limit": step.time_limit,
                    "created_date": step.created_date,
                    "last_modified": step.last_modified,
                }
                for step in instance.steps.order_by("order")
            ]

        data["workflow_steps"] = [
            {
                "id": w_step.pk,
                "order": w_step.order,
                "created_date": w_step.created_date,
                "condition": w_step.condition_type,
            }
            for w_step in instance.workflow_steps()
        ]
        return data


class RequisitionWorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = ("id", "order", "step_id", "workflow_id")


class RequisitionWorkflowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = (
            "id",
            "name",
            "description",
        )
