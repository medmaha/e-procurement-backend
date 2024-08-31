from datetime import date
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from apps.organization.models import (
    DepartmentProcurementPlan,
    AnnualPlan,
)
from apps.organization.api.serializers.plan import (
    PlanItemSelectSerializer,
)


class DepartmentProcurementPlansSelectView(ListAPIView):
    "List all plans items under this department for the current_annual_plan"

    serializer_class = PlanItemSelectSerializer

    def get_queryset(self):
        year = date.today().year
        annual_plan = AnnualPlan.objects.filter(year_start__year=year).first()
        if not annual_plan:
            return []
        department_id = self.request.query_params.get("department_id")  # type: ignore
        plans: DepartmentProcurementPlan = annual_plan.department_plans.filter(department__id=int(department_id)).first()  # type: ignore
        if not plans:
            return []
        return plans.items.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({"data": serializer.data})
