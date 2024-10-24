from django.db.models import Count

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.procurement.models import ApprovalStep


class ApprovalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = (
            "id",
            "name",
            "description",
            "order",
            "role",
            "remarks",
            "is_final",
            "is_optional",
            "time_limit",
            "created_date",
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
            data["officer"] = {
                "id": instance.approver.pk,
                "name": instance.approver.name,
            }

        if instance.workflow:
            data["workflow"] = {
                "id": instance.workflow.pk,
                "name": instance.workflow.name,
            }

        return data


class RequisitionApprovalStepAPIView(APIView):

    def get(self, request, approval_step_id=None, *args, **kwargs):

        if approval_step_id:
            workflows = ApprovalStep.objects.filter(id=approval_step_id)
        else:
            workflows = ApprovalStep.objects.all()

        serializer = ApprovalStepSerializer(
            workflows,
            many=approval_step_id is None,
            context={"request": request, "approval_step_id": approval_step_id},
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
