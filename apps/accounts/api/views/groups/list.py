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

        auth_perms = {
            "create": AuthGroup.has_perm(request.user, "add"),
            "read": AuthGroup.has_perm(request.user, "view"),
            "update": AuthGroup.has_perm(request.user, "change"),
            "delete": AuthGroup.has_perm(request.user, "delete"),
        }

        return Response({"data": serializer.data, "auth_perms": auth_perms})


class GroupListSelectView(ListAPIView):
    serializer_class = GroupSelectSerializer
    queryset = Group.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
