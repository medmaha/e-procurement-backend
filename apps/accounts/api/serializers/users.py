from rest_framework import serializers
from apps.accounts.models import Account


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "full_name",
            "is_active",
            "created_date",
            "profile_type",
        ]


class AccountQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "avatar",
            "full_name",
            "profile_type",
            "created_date",
        ]


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "avatar",
            "phone_number",
            "created_date",
            "password",
        ]


class AccountRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "avatar",
            "full_name",
            "phone_number",
            "created_date",
        ]


class AccountUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Account
        fields = [
            "email",
            "last_name",
            "first_name",
            "middle_name",
            "phone_number",
        ]
