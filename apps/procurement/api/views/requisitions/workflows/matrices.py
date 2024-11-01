from decimal import Decimal
from django.db import transaction
from django.db.models import Count

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.organization.models.department import Department
from apps.organization.models.unit import Unit
from apps.procurement.api.serializers.requisition_workflow import (
    RequisitionMatrixReadSerializer,
    RequisitionMatrixMutateSerializer,
)
from apps.procurement.models import ApprovalMatrix, ApprovalWorkflow


class ApprovalMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalMatrix
        fields = (
            "id",
            "min_amount",
            "max_amount",
            "workflow",
            "created_date",
            "last_modified",
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


class RequisitionApprovalMatrixAPIView(APIView):

    def get(self, request, matrix_id=None, *args, **kwargs):

        try:
            if matrix_id:
                matrix_id = int(matrix_id)
                matrices = ApprovalMatrix.objects.get(id=matrix_id)
            else:
                matrices = ApprovalMatrix.objects.all()

            serializer = ApprovalMatrixSerializer(
                instance=matrices,
                many=matrix_id is None,
                context={"request": request, "matrix_id": matrix_id},
            )

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except ApprovalMatrix.DoesNotExist:
            return Response(
                {"message": "Matrix does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"message": "Invalid matrix id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                data = request.data.copy()
                serializer = RequisitionMatrixMutateSerializer(data=data)

                if serializer.is_valid():
                    profile = request.user.profile
                    matrix = serializer.save(author=profile)
                    matrix_serializer = RequisitionMatrixReadSerializer(
                        instance=matrix,
                        context={"request": request, "matrix_id": matrix.pk},
                    )
                    return Response(
                        {"data": matrix_serializer.data}, status=status.HTTP_201_CREATED
                    )

                raise serializers.ValidationError(serializer.errors)

        except Exception as e:
            return Response(
                {"message": e.__str__()}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, matrix_id, *args, **kwargs):

        try:
            matrix = ApprovalMatrix.objects.get(id=matrix_id)
            profile = request.user.profile

            with transaction.atomic():
                data = request.data.copy()
                serializers = RequisitionMatrixMutateSerializer(
                    instance=matrix, data=data
                )

                if serializers.is_valid():
                    matrix = serializers.save(author=profile)
                    matrix_serializer = RequisitionMatrixReadSerializer(
                        instance=matrix,
                        context={"request": request, "matrix_id": matrix_id},
                    )
                    return Response(
                        {"data": matrix_serializer.data}, status=status.HTTP_200_OK
                    )

                raise Exception("Invalid matrix form-data")

        except ApprovalMatrix.DoesNotExist:
            return Response(
                {"message": "Matrix does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"message": e.__str__()}, status=status.HTTP_400_BAD_REQUEST
            )
