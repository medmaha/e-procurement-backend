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

    def get_queryset(self, is_superuser: bool):

        if not is_superuser:
            return Account.objects.filter(is_superuser=False, is_active=True)

        return Account.objects.filter()

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        queryset = self.get_queryset(user.is_superuser)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
