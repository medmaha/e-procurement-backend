from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.accounts.models import AuthGroup
from django.contrib.auth.models import Group
from apps.accounts.api.serializer.group import (
    GroupListSerializer,
    GroupSelectSerializer,
)


class GroupListView(ListAPIView):
    serializer_class = GroupListSerializer

    def get_queryset(self):
        apps = ["organization", "procurement", "accounts", "vendors"]
        return AuthGroup.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        groups = request.user.groups.all()

        auth_perms = {
            "create": request.user.has_perm("accounts.add_authgroup"),
            "read": request.user.has_perm("accounts.view_authgroup"),
            "update": request.user.has_perm("accounts.change_authgroup"),
            "delete": request.user.has_perm("accounts.delete_authgroup"),
        }
        return Response({"data": serializer.data, "auth_perms": auth_perms})


class GroupListSelectView(ListAPIView):
    serializer_class = GroupSelectSerializer
    queryset = Group.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
