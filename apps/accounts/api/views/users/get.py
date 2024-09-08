from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.accounts.models import Account
from apps.organization.api.serializers.staff import StaffRetrieveSerializer
from apps.core.utilities.generators import revert_unique_id


class AccountSerializer(serializers.ModelSerializer):
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
            "created_date",
        ]


class AccountGetView(RetrieveAPIView):
    def retrieve(self, request, user_id, *args, **kwargs):
        account = get_object_or_404(Account, pk=user_id)
        profile_type, profile = account.get_profile()

        account_serializer: dict = AccountSerializer(
            account, context={"request": request}
        ).data  # type: ignore

        profile_serializer: dict = {}
        if profile_type == "Staff":
            profile_serializer = StaffRetrieveSerializer(
                profile, context={"request": request}
            ).data  # type: ignore

        return Response(
            {
                **account_serializer,
                **profile_serializer,
                "profile_type": profile_type,
            },
            status=status.HTTP_200_OK,
        )
