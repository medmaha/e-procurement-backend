from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.accounts.models import Account
from apps.organization.api.serializers.staff import StaffRetrieveSerializer
from apps.core.utilities.generators import revert_generated_unique_id


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


class AccountRetrieveView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        user_id = revert_generated_unique_id(
            None, kwargs.get("user_id") or request.user.id
        )
        account = get_object_or_404(Account, pk=user_id)
        profile_type, profile = account.get_profile()

        account_serializer = AccountSerializer(
            account, context={"request": request}
        ).data

        profile_serializer: dict = {}
        if profile_type == "Staff":
            profile_serializer = StaffRetrieveSerializer(
                profile, context={"request": request}
            ).data  # type: ignore

        return Response(
            {
                "data": {
                    "account": account_serializer,
                    "profile": {
                        **profile_serializer,
                        "profile_type": profile_type,
                    },
                }
            },
            status=status.HTTP_200_OK,
        )
