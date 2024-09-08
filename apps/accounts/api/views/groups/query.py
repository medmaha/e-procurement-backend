from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.accounts.models import AuthGroup
from apps.accounts.serializer.group import (
    GroupListSerializer,
)


class GroupQueryAPIView(ListAPIView):
    serializer_class = GroupListSerializer

    def get_queryset(self, q: str):
        return AuthGroup.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")

        if not q:
            return Response({"results": [], "count": 0})

        queryset = self.get_queryset(q)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
