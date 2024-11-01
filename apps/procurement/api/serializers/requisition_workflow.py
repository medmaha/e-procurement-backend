from rest_framework import serializers


from apps.procurement.models import (
    ApprovalWorkflow,
    WorkflowStep,
    ApprovalStep,
    ApprovalMatrix,
)


class RequisitionMatrixMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalMatrix
        fields = (
            "unit",
            "status",
            "workflow",
            "min_amount",
            "max_amount",
            "department",
            "description",
        )


class RequisitionMatrixReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalMatrix
        fields = (
            "id",
            "unit",
            "status",
            "workflow",
            "min_amount",
            "max_amount",
            "department",
            "description",
        )

    def to_representation(self, instance: ApprovalMatrix):
        data = super().to_representation(instance)

        matrix_id = self.context.get("matrix_id")

        if instance.department:
            data["department"] = {
                "id": instance.department.pk,
                "name": instance.department.name,
            }
        if instance.unit:
            data["unit"] = {
                "id": instance.unit.pk,
                "name": instance.unit.name,
            }

        if instance.workflow:
            data["workflow"] = {
                "id": instance.workflow.pk,
                "name": instance.workflow.name,
            }

            if matrix_id:
                data["workflow"]["created_date"] = instance.workflow.created_date
                data["workflow"]["last_modified"] = instance.workflow.last_modified
                data["workflow"]["workflow_steps"] = [
                    {
                        "id": w_step.pk,
                        "order": w_step.order,
                        "created_date": w_step.created_date,
                        "condition": w_step.condition_type,
                        "step": {
                            "id": w_step.step.pk,
                            "order": w_step.step.order,
                            "name": w_step.step.name,
                            "role": w_step.step.role,
                            "description": w_step.step.description,
                            "department": (
                                {
                                    "id": w_step.step.department.pk,
                                    "name": w_step.step.department.name,
                                }
                                if w_step.step.department
                                else None
                            ),
                            "approver": (
                                {
                                    "id": w_step.step.approver.pk,
                                    "name": w_step.step.approver.name,
                                    "job_title": w_step.step.approver.job_title,
                                }
                                if w_step.step.approver
                                else None
                            ),
                            "remarks": w_step.step.remarks,
                            "is_final": w_step.step.is_final,
                            "is_optional": w_step.step.is_optional,
                            "time_limit": w_step.step.time_limit,
                            "created_date": w_step.step.created_date,
                            "last_modified": w_step.step.last_modified,
                        },
                    }
                    for w_step in instance.workflow.workflow_steps()
                ]

        if instance.author:
            data["author"] = {
                "id": instance.author.pk,
                "name": instance.author.name,
                "job_title": instance.author.job_title,
                "avatar": instance.author.user_account.avatar,
            }

        return data


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

        data["workflow_steps"] = [
            {
                "id": w_step.pk,
                "order": w_step.order,
                "created_date": w_step.created_date,
                "condition": w_step.condition_type,
                "step": {
                    "id": w_step.step.pk,
                    "order": w_step.step.order,
                    "name": w_step.step.name,
                    "role": w_step.step.role,
                    "description": w_step.step.description,
                    "department": (
                        {
                            "id": w_step.step.department.pk,
                            "name": w_step.step.department.name,
                        }
                        if w_step.step.department
                        else None
                    ),
                    "officer": (
                        {
                            "id": w_step.step.approver.pk,
                            "name": w_step.step.approver.name,
                        }
                        if w_step.step.approver
                        else None
                    ),
                    "remarks": w_step.step.remarks,
                    "is_final": w_step.step.is_final,
                    "is_optional": w_step.step.is_optional,
                    "time_limit": w_step.step.time_limit,
                    "created_date": w_step.step.created_date,
                    "last_modified": w_step.step.last_modified,
                },
            }
            for w_step in instance.workflow_steps()
        ]
        return data


class WorkflowStepMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = (
            "step",
            "order",
            "condition_type",
            "condition_value",
        )


class WorkflowStepReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = (
            "id",
            "order",
            "step",
            "workflow",
            "condition_type",
            "condition_value",
            "created_date",
            "last_modified",
        )

    def to_representation(self, instance: WorkflowStep):
        data = super().to_representation(instance)

        data["step"] = (
            {
                "id": instance.step.pk,
                "order": instance.step.order,
                "name": instance.step.name,
                "role": instance.step.role,
                "description": instance.step.description,
                "department": (
                    {
                        "id": instance.step.department.pk,
                        "name": instance.step.department.name,
                    }
                    if instance.step.department
                    else None
                ),
                "approver": (
                    {
                        "id": instance.step.approver.pk,
                        "name": instance.step.approver.name,
                        "job_title": instance.step.approver.job_title,
                    }
                    if instance.step.approver
                    else None
                ),
                "remarks": instance.step.remarks,
                "is_final": instance.step.is_final,
                "is_optional": instance.step.is_optional,
                "time_limit": instance.step.time_limit,
                "created_date": instance.step.created_date,
                "last_modified": instance.step.last_modified,
            },
        )


class WorkflowMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = (
            "name",
            "status",
            "description",
        )


class ApprovalStepMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = (
            "name",
            "role",
            "order",
            "remarks",
            "description",
            "is_optional",
            "approver",
            "department",
        )
