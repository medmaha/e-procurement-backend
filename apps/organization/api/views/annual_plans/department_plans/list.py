from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import (
    DepartmentProcurementPlan,
)
from apps.organization.api.serializers.plan import (
    DepartmentProcurementPlanListSerializer,
)
from apps.accounts.models import Account
from apps.procurement.models.requisition import Requisition


class DepartmentProcurementPlanListView(ListAPIView):
    serializer_class = DepartmentProcurementPlanListSerializer

    def get_queryset(self):
        queryset = DepartmentProcurementPlan.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        requisition_id = request.query_params.get("requisition_id")

        auth_perms = {
            "create": request.user.has_perm("organization.add_annualprocurementplan")
        }

        many = True

        if requisition_id:
            error = lambda: Response(
                {"message": "Can't find a department for this requisition"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            try:
                int(requisition_id)
                requisition = Requisition.objects.get(id=requisition_id)
                department = (
                    requisition.officer.unit.department if requisition.officer else None
                )
                if not department:
                    return error()
                queryset = DepartmentProcurementPlan.objects.filter(
                    department=department
                ).first()
                if not queryset:
                    return Response(
                        {
                            "data": {
                                "department": {
                                    "name": department.name,
                                    "description": department.description,
                                }
                            },
                        }
                    )
                many = False
            except Exception as e:
                return error()
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=many)
        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
            status=status.HTTP_200_OK,
        )
