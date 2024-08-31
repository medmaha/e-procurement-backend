from datetime import date
from django.db import transaction
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.api.serializers.plan import (
    AnnualPlanCreateSerializer,
)
from apps.accounts.models import Account
from apps.organization.models.procurement_plan import (
    AnnualPlan,
)
from apps.core.utilities.errors import get_serializer_error_message


class AnnuaLPlanCreateView(CreateAPIView):
    serializer_class = AnnualPlanCreateSerializer

    def create(self, request, *args, **kwargs):
        user: Account = request.user

        if not user.has_perm("organization.add_annualplan"):
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to create a annual procurement plan",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile_name, profile = user.get_profile()

        exists = AnnualPlan.objects.filter(
            year_start=request.data.get("year_start") or timezone.now()
        ).exists()

        if exists:
            return Response(
                {
                    "success": False,
                    "message": "An annual procurement plan already exists for this year",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            annual_plan = AnnualPlan.get_current_plan()
            with transaction.atomic():
                new_annual_plan = serializer.save(officer=profile)
                if annual_plan:
                    if new_annual_plan.year_start.year >= annual_plan.year_start.year:
                        AnnualPlan.objects.filter(pk__neq=new_annual_plan.pk).update(
                            is_current_plan=False,
                            is_operational=False,
                        )
                        if new_annual_plan.is_current_plan:
                            AnnualPlan.objects.filter(
                                pk__neq=new_annual_plan.pk
                            ).update(
                                is_current_plan=False,
                                is_operational=False,
                            )
                return Response(
                    {
                        "success": True,
                        "message": "Annual Plan created successfully",
                    }
                )
        return Response(
            {
                "success": False,
                "message": get_serializer_error_message(serializer),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
