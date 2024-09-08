from rest_framework import serializers
from apps.accounts.models import AuthGroup
from django.contrib.auth.models import Group, Permission


class GroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthGroup
        fields = [
            "id",
            "name",
            "description",
            "editable",
            "authored_by",
            "company_id",
            "group_id",
        ]


class GroupUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = AuthGroup
        fields = [
            "name",
            "description",
        ]


class GroupListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = AuthGroup
        exclude = ["created_date"]

    def get_permissions(self, obj):
        try:
            return (
                Group.objects.get(name=obj.name)
                .permissions.all()
                .values("id", "name", "codename")
            )
        except:
            return []


class GroupRetrieveSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = AuthGroup
        fields = [
            "id",
            "name",
            "description",
            "editable",
            "authored_by",
            "created_date",
            "last_modified",
            "permissions",
        ]

    def get_permissions(self, obj):
        try:
            return (
                Group.objects.get(name=obj.name)
                .permissions.all()
                .values("id", "name", "codename")
            )
        except:
            return []


class GroupSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
