from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from apps.organization.models import (
    DepartmentProcurementPlan,
)
from apps.organization.api.serializers.plan import (
    DepartmentProcurementPlanListSerializer,
)


class DepartmentProcurementPlansSelectView(ListAPIView):
    "List all plans items under this department for the current_annual_plan"

    serializer_class = DepartmentProcurementPlanListSerializer

    def get_queryset(self, department_id):
        plan = get_object_or_404(DepartmentProcurementPlan, department_id=department_id)
        return plan.items.all()

    def list(self, request, *args, **kwargs):
        department_id = request.query_params.get("department_id")
        queryset = self.get_queryset(department_id)
        serializer = self.get_serializer(queryset, many=True)

        return Response({"data": serializer.data})
