from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Unit
from apps.organization.api.serializers.unit import (
    UnitListSerializer,
)
from apps.accounts.models import Account


class UnitListView(ListAPIView):
    serializer_class = UnitListSerializer

    def get_queryset(self):
        queryset = Unit.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        auth_perms = {
            "create": request.user.has_perm("organization.add_unit"),
            "read": request.user.has_perm("organization.view_unit"),
            "update": request.user.has_perm("organization.change_unit"),
            "delete": request.user.has_perm("organization.delete_unit"),
        }
        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
            status=status.HTTP_200_OK,
        )
