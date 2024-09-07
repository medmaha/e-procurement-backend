from rest_framework import serializers
from apps.accounts.models import AuthGroup
from django.contrib.auth.models import Group, Permission


class GroupCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = AuthGroup
        exclude = ["name", "description"]


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


class GroupSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
