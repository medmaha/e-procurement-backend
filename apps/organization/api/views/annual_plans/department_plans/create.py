from decimal import Decimal
from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Department
from apps.organization.api.serializers.plan import (
    PlanItemListSerializer,
    DepartmentProcurementPlanCreateSerializer,
)
from apps.accounts.models import Account
from apps.organization.models.procurement_plan import (
    AnnualPlan,
    DepartmentProcurementPlan,
)
from apps.core.utilities.errors import get_serializer_error_message


class DepartmentProcurementPlanCreateView(CreateAPIView):
    serializer_class = DepartmentProcurementPlanCreateSerializer

    def create(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        # if not request.user.has_perm("organization.add_departmentprocurementplan"):
        #     return Response(
        #         {
        #             "success": False,
        #             "message": "You do not have permission to create a plan",
        #         },
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        annual_plan = AnnualPlan.get_plan_by_year(request.query_params.get("year"))

        if not annual_plan:
            return Response(
                {
                    "success": False,
                    "message": "No annual plan found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        plan_data = request.data.copy()
        department_plan_items_data = (
            plan_data.pop("items") if "items" in plan_data else None
        )

        if not department_plan_items_data:
            return Response(
                {
                    "success": False,
                    "message": "A plan must include at least one item",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        for item in department_plan_items_data:
            # TODO: don't trust the client site validation
            item.update(
                {
                    "quantity": item.get("quantity") or None,
                    "quarter_1_budget": item.get("quarter_1_budget") or Decimal(0),
                    "quarter_2_budget": item.get("quarter_2_budget") or Decimal(0),
                    "quarter_3_budget": item.get("quarter_3_budget") or Decimal(0),
                    "quarter_4_budget": item.get("quarter_4_budget") or Decimal(0),
                }
            )
        department = Department.objects.filter(
            id=plan_data.pop("department_id") if "department_id" else 0
        ).first()
        if not department:
            return Response({"message": "The selected department is invalid"})

        department_plan_item_serializer = PlanItemListSerializer(
            data=department_plan_items_data, many=True
        )
        instance = DepartmentProcurementPlan.objects.filter(
            department=department,
            annual_plan=annual_plan,  # this is a reverse query
        ).first()
        department_plan_serializer = self.get_serializer(
            instance=instance, data=plan_data
        )

        if department_plan_serializer.is_valid():
            if department_plan_item_serializer.is_valid():
                with transaction.atomic():
                    department_plan = department_plan_serializer.save(
                        department=department
                    )
                    department_plan.items.add(*department_plan_item_serializer.save())
                    annual_plan.department_plans.add(department_plan)
                    return Response(
                        {
                            "message": "Procurement Plan created successfully",
                            "success": True,
                        },
                        status=status.HTTP_201_CREATED,
                    )
            return Response(
                {
                    "success": False,
                    "message": get_serializer_error_message(
                        department_plan_item_serializer
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": False,
                "message": get_serializer_error_message(department_plan_serializer),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
