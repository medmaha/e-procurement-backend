from django.db.models import Count

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.procurement.models import ApprovalMatrix


class ApprovalMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalMatrix
        fields = (
            "id",
            "min_amount",
            "max_amount",
            "unit",
            "department",
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
        if instance.author:
            data["author"] = {
                "id": instance.author.pk,
                "name": instance.author.name,
            }

        return data


class RequisitionApprovalMatrixAPIView(APIView):

    def get(self, request, matrix_id=None, *args, **kwargs):

        if matrix_id:
            matrices = ApprovalMatrix.objects.filter(id=matrix_id)
        else:
            matrices = ApprovalMatrix.objects.all()

        serializer = ApprovalMatrixSerializer(
            matrices,
            many=matrix_id is None,
            context={"request": request, "matrix_id": matrix_id},
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
