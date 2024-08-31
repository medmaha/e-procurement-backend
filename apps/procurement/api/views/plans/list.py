from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models.procurement_plan import DepartmentProcurementPlan
from apps.procurement.api.serializers.plan import ProcurementPlanListSerializer
from apps.procurement.models.requisition import Requisition
from apps.organization.models.department import Department


class ProcurementPlanListView(ListAPIView):
    serializer_class = ProcurementPlanListSerializer

    def get_queryset(self):
        queryset = DepartmentProcurementPlan.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user = request.user
        profile_name, profile = user.profile

        requisition_id = request.query_params.get("requisition_id")

        if requisition_id:
            try:
                int(requisition_id)
                requisition = Requisition.objects.get(id=requisition_id)
                department = (
                    requisition.officer.unit.department if requisition.officer else None
                )
                if not department:
                    raise Exception("department not found")
                queryset = DepartmentProcurementPlan.objects.filter(
                    department=department
                )
            except Exception as e:
                print(e)
                requisition_id = None
                queryset = self.get_queryset()
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(instance=queryset, many=not requisition_id)

        return Response(serializer.data, status=status.HTTP_200_OK)
