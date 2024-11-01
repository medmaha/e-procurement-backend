from django.db import transaction
from django.db.models import Count

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.core.utilities.errors import get_serializer_error_message
from apps.procurement.models import ApprovalStep
from apps.procurement.api.serializers.requisition_workflow import (
    ApprovalStepMutateSerializer,
)


class ApprovalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = (
            "id",
            "name",
            "order",
            "role",
            "remarks",
            "is_final",
            "time_limit",
            "is_optional",
            "description",
            "created_date",
            "last_modified",
        )

    def to_representation(self, instance: ApprovalStep):
        data = super().to_representation(instance)

        approval_step_id = self.context.get("approval_step_id")

        if instance.department:
            data["department"] = {
                "id": instance.department.pk,
                "name": instance.department.name,
            }

        if instance.approver:
            data["approver"] = {
                "id": instance.approver.pk,
                "name": instance.approver.name,
                "job_title": instance.approver.job_title,
                "unit": (
                    {
                        "id": instance.approver.unit.pk,
                        "name": instance.approver.unit.name,
                        "department": {
                            "id": instance.approver.department.pk,
                            "name": instance.approver.department.name,
                        },
                    }
                    if approval_step_id is not None
                    else None
                ),
            }

        # if instance.workflow:
        #     data["workflow"] = {
        #         "id": instance.workflow.pk,
        #         "name": instance.workflow.name,
        #     }

        return data


class RequisitionApprovalStepAPIView(APIView):

    def get(self, request, approval_step_id=None, *args, **kwargs):
        try:
            if approval_step_id:
                workflows = ApprovalStep.objects.get(id=approval_step_id)
            else:
                workflows = ApprovalStep.objects.all()
            serializer = ApprovalStepSerializer(
                instance=workflows,
                many=approval_step_id is None,
                context={"request": request, "approval_step_id": approval_step_id},
            )

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except ApprovalStep.DoesNotExist:
            return Response(
                {"message": "approval-step not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            print(e)
            return Response(
                {"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        try:
            serializer = ApprovalStepMutateSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                step = serializer.save()
                approval_step_serializer = ApprovalStepSerializer(
                    instance=step, context={"request": request}
                )
                return Response(
                    {"data": approval_step_serializer.data},
                    status=status.HTTP_201_CREATED,
                )

            error_message = get_serializer_error_message(serializer)
            raise Exception(error_message)

        except Exception as e:
            return Response(
                {"message": e.__str__()}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, *args, **kwargs):
        try:

            with transaction.atomic():
                data: dict = request.data.copy()

                steps = data.pop("steps", None)

                if steps and isinstance(steps, list):
                    for step in steps:
                        order = step.get("order", 0)
                        _step_id = step.get("id", None)

                        if _step_id and order:
                            step = ApprovalStep.objects.select_for_update().get(
                                id=_step_id
                            )
                            step.order = order
                            step.save()

                            continue

                        raise Exception(f"Invalid data {step}", code=400)

                    return Response(
                        {"message": "Reordered successfully"}, status=status.HTTP_200_OK
                    )

                step_id: str = data.pop("id", 0)

                step = ApprovalStep.objects.get(id=step_id)

                profile = request.user.profile

                if step.author and step.author != profile:
                    return Response(
                        {"message": "You are not authorized to perform this action"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                serializer = ApprovalStepMutateSerializer(
                    instance=step, data=request.data, context={"request": request}
                )

                if serializer.is_valid():
                    step = serializer.save(author=profile)
                    approval_step_serializer = ApprovalStepSerializer(
                        instance=step, context={"request": request}
                    )
                    return Response(
                        {"data": approval_step_serializer.data},
                        status=status.HTTP_200_OK,
                    )
                error_message = get_serializer_error_message(serializer)
                raise Exception(error_message)

        except ApprovalStep.DoesNotExist:
            return Response(
                {"message": "Approval Step does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except serializers.ValidationError as e:
            return Response(
                {"message": e.__str__()}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
