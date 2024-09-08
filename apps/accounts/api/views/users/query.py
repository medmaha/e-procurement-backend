from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.accounts.models import Account

from ...serializers.users import AccountQuerySerializer


class AccountQueryView(ListAPIView):
    serializer_class = AccountQuerySerializer

    def get_queryset(self, q: str):
        return Account.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
        )

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        if not q:
            return Response([])

        queryset = self.get_queryset(q)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
