from datetime import date
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import (
    AnnualPlan,
)
from apps.organization.api.serializers.plan import (
    AnnualPlanRetrieveSerializer,
)
from apps.accounts.models import Account


class AnnualPlanRetrieveView(RetrieveAPIView):
    serializer_class = AnnualPlanRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        user: Account = request.user
        profile_type, profile = user.get_profile()

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
        auth_perms = {"create": request.user.has_perm("organization.add_annualplan")}

        if current_plan:
            serializer = self.get_serializer(
                instance=current_plan, context={"request": request}
            )
            return Response(
                {"data": serializer.data, "auth_perms": auth_perms},
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": "No plan found for this year",
                "auth_perms": auth_perms,
            },
            status=status.HTTP_200_OK,
        )
