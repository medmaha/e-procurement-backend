from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Staff
from apps.organization.api.serializers.staff import (
    StaffListSerializer,
)
from apps.accounts.models import Account


class StaffListView(ListAPIView):
    serializer_class = StaffListSerializer

    def get_queryset(self):
        queryset = Staff.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        auth_perms = {
            "create": request.user.has_perm("organization.add_staff"),
            "read": request.user.has_perm("organization.view_staff"),
            "update": request.user.has_perm("organization.change_staff"),
            "delete": request.user.has_perm("organization.delete_staff"),
        }

        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
            status=status.HTTP_200_OK,
        )
