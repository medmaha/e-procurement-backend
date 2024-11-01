from django.db import transaction

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.procurement.models import ApprovalWorkflow, WorkflowStep, ApprovalStep
from apps.procurement.api.serializers.requisition_workflow import (
    WorkflowMutateSerializer,
    WorkflowStepReadSerializer,
    WorkflowStepMutateSerializer,
)


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = (
            "id",
            "name",
            "status",
            "description",
            "created_date",
            "last_modified",
        )

    def to_representation(self, instance: ApprovalWorkflow):
        data = super().to_representation(instance)

        if instance.author:
            data["author"] = {
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
            for w_step in instance.workflow_steps()
        ]
        return data


class RequisitionWorkflowAPIView(APIView):

    def get(self, request, workflow_id=None, *args, **kwargs):

        if workflow_id:
            workflows = ApprovalWorkflow.objects.select_related("author").get(
                id=workflow_id
            )
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
            data = request.data.copy()
            with transaction.atomic():
                workflow_steps = data.pop("workflow_steps", [])
                serializer = WorkflowMutateSerializer(
                    data=data, context={"request": request}
                )
                profile = request.user.profile
                if serializer.is_valid():
                    workflow = serializer.save(author=profile)
                    for step in workflow_steps:
                        step["workflow"] = workflow.pk
                        step_serializer = WorkflowStepMutateSerializer(
                            data=step, context={"request": request}
                        )
                        if step_serializer.is_valid():
                            step_serializer.save(workflow=workflow, author=profile)
                        else:
                            print("Error: Step Serializer", step_serializer.errors)
                            raise serializers.ValidationError(
                                step_serializer.errors, code=400
                            )

                    return Response(
                        {"data": step_serializer.data}, status=status.HTTP_201_CREATED
                    )
                print("Error: Main Serializer", serializer.errors)
                raise serializers.ValidationError(serializer.errors, code=400)

        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, workflow_id, *args, **kwargs):
        try:
            workflow_step = ApprovalWorkflow.objects.only("id").get(pk=workflow_id)
            profile = request.user.profile

            data = request.data.copy()

            with transaction.atomic():
                workflow_steps = data.pop("workflow_steps", [])
                serializer = WorkflowMutateSerializer(
                    instance=workflow_step, data=data, context={"request": request}
                )

                if serializer.is_valid():

                    workflow_step = serializer.save(author=profile)

                    for workflow_step_data in workflow_steps:

                        print(workflow_step_data)

                        _step = None
                        _workflow_step = None
                        step_id = workflow_step_data.get("step")
                        workflow_step_id = workflow_step_data.get("id")

                        if workflow_step_id:
                            _workflow_step = WorkflowStep.objects.only("id").get(
                                pk=workflow_step_id
                            )

                        if _workflow_step:
                            if isinstance(step_id, dict):
                                step_id = step_id.get("id")
                            _step = ApprovalStep.objects.only("id").get(pk=step_id)
                            workflow_step_data["step"] = _step.pk

                        step_serializer = WorkflowStepMutateSerializer(
                            instance=_workflow_step,
                            data=workflow_step_data,
                            context={"request": request},
                        )

                        if step_serializer.is_valid():
                            step_serializer.save(
                                workflow=(
                                    _workflow_step.workflow
                                    if _workflow_step
                                    else workflow_step
                                ),
                                author=profile,
                            )
                        else:
                            print("Step:", step_serializer.errors)
                            raise serializers.ValidationError(
                                step_serializer.errors, code=400
                            )

                    workflow_step_serializer = ApprovalWorkflowSerializer(
                        instance=workflow_step
                    )

                    return Response(
                        {"data": workflow_step_serializer.data},
                        status=status.HTTP_201_CREATED,
                    )
                raise serializers.ValidationError(serializer.errors, code=400)

        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
