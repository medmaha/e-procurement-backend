from django.db.models import Count

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.procurement.models.requisition_approval_workflow import ApprovalWorkflow


count = 0


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = ("id", "name", "description", "created_date", "last_modified")

    def to_representation(self, instance: ApprovalWorkflow):
        data = super().to_representation(instance)

        if instance.officer:
            data["officer"] = {
                "id": instance.officer.pk,
                "name": instance.officer.name,
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
                            "id": step.officer.pk,
                            "name": step.officer.name,
                        }
                        if step.officer
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
                "name": w_step.__str__(),
                "order": w_step.order,
                "created_date": w_step.created_date,
                "last_modified": w_step.last_modified,
                "step": {
                    "id": w_step.step.pk,
                    "order": w_step.step.order,
                    "name": w_step.step.name,
                    "is_final": w_step.step.is_final,
                    "is_optional": w_step.step.is_optional,
                    "time_limit": w_step.step.time_limit,
                    "created_date": w_step.step.created_date,
                    "last_modified": w_step.step.last_modified,
                },
                "condition": w_step.condition,
            }
            for w_step in instance.workflow_steps()
        ]
        return data


class RequisitionWorkflowAPIView(APIView):

    def get(self, request, workflow_id=None, *args, **kwargs):

        if workflow_id:
            workflows = ApprovalWorkflow.objects.get(id=workflow_id)
        else:
            workflows = ApprovalWorkflow.objects.filter(type="requisition")

        serializer = ApprovalWorkflowSerializer(
            workflows,
            many=workflow_id is None,
            context={"request": request, "workflow_id": workflow_id},
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
