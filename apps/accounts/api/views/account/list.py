from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.accounts.models import Account


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "is_active",
            "profile_type",
            "last_login",
            "created_date",
        ]


class AccountListView(ListAPIView):
    serializer_class = AccountListSerializer

    def get_queryset(self):
        return Account.objects.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
