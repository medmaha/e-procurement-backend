from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.accounts.models import Account

from ...serializers.users import AccountListSerializer


class AccountListView(ListAPIView):
    serializer_class = AccountListSerializer

    def get_queryset(self):
        return Account.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
