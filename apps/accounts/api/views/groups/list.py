from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.accounts.models import AuthGroup
from django.contrib.auth.models import Group
from apps.accounts.serializer.group import (
    GroupListSerializer,
    GroupSelectSerializer,
)


class GroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer

    def get_queryset(self):
        return AuthGroup.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GroupListSelectView(ListAPIView):
    serializer_class = GroupSelectSerializer
    queryset = Group.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
