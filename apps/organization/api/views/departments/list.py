from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Department
from apps.organization.api.serializers.department import DepartmentListSerializer
from apps.accounts.models import Account


class DepartmentListView(ListAPIView):
    serializer_class = DepartmentListSerializer

    def get_queryset(self):
        queryset = Department.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        auth_perms = {
            "create": request.user.has_perm("organization.add_department"),
            "read": request.user.has_perm("organization.view_department"),
            "update": request.user.has_perm("organization.change_department"),
            "delete": request.user.has_perm("organization.delete_department"),
        }
        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
            status=status.HTTP_200_OK,
        )
