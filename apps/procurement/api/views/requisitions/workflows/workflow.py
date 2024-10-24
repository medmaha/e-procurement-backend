from django.db import transaction

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.procurement.models import ApprovalWorkflow
from apps.procurement.api.serializers.requisition_workflow import (
    RequisitionWorkflowCreateSerializer,
    RequisitionWorkflowStepSerializer,
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
                "condition": w_step.condition_type,
            }
            for w_step in instance.workflow_steps()
        ]
        return data


class RequisitionWorkflowAPIView(APIView):

    def get(self, request, workflow_id=None, *args, **kwargs):

        if workflow_id:
            workflows = ApprovalWorkflow.objects.get(id=workflow_id)
        else:
            workflows = ApprovalWorkflow.objects.filter()

        serializer = ApprovalWorkflowSerializer(
            workflows,
            many=workflow_id is None,
            context={"request": request, "workflow_id": workflow_id},
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                workflow_steps = request.data.pop("workflow_steps", None)
                serializer = RequisitionWorkflowCreateSerializer(
                    data=request.data, context={"request": request}
                )
                if serializer.is_valid():
                    workflow = serializer.save()
                    for step in workflow_steps:
                        serializer = RequisitionWorkflowStepSerializer(
                            data=step, context={"request": request}
                        )
                        if serializer.is_valid():
                            serializer.save(workflow=workflow)
                        else:
                            raise serializers.ValidationError(
                                serializer.errors, code=400
                            )
                    return Response(
                        {"data": serializer.data}, status=status.HTTP_201_CREATED
                    )
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
