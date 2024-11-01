from datetime import date
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import AnnualPlan, DepartmentProcurementPlan
from apps.organization.api.serializers.plan import (
    AnnualPlanRetrieveSerializer,
)


class AnnualPlanRetrieveView(RetrieveAPIView):
    serializer_class = AnnualPlanRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        profile_type = request.user.profile_type

        if profile_type.lower() != "staff":
            return Response(
                {"message": "You're forbidden for this request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = date.today()
        year = request.query_params.get("year")

        try:
            if year:
                year = int(year)
            if year and year > today.year:
                raise ValueError("Invalid year provided")
        except Exception as e:
            return Response(
                {"message": "Invalid year provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not year:
            query = {"year_start__year": today.year}
        elif year and year == today.year:
            query = {"year_start__year": year}
        else:
            query = {"year_start__year__lte": year}

        current_plan = AnnualPlan.objects.filter(**query).first()
        # auth_perms = {"create": True}
        auth_perms = {
            "create": request.user.has_perm(
                f"{AnnualPlan._meta.app_label}.add_{AnnualPlan._meta.model_name}"
            ),
            "update": request.user.has_perm(
                f"{AnnualPlan._meta.app_label}.change_{AnnualPlan._meta.model_name}"
            ),
        }

        if current_plan:
            dept_perms = {
                "create": request.user.has_perm(
                    f"{DepartmentProcurementPlan._meta.app_label}.add_{DepartmentProcurementPlan._meta.model_name}"
                ),
                "update": request.user.has_perm(
                    f"{DepartmentProcurementPlan._meta.app_label}.change_{DepartmentProcurementPlan._meta.model_name}"
                ),
            }
            serializer = self.get_serializer(
                instance=current_plan, context={"request": request}
            )
            return Response(
                {
                    "data": serializer.data,
                    "auth_perms": auth_perms,
                    "extras": {"dept_perms": dept_perms},
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": "No plan found for this year",
                "auth_perms": auth_perms,
            },
            status=status.HTTP_200_OK,
        )
