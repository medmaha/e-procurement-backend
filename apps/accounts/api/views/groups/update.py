from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.accounts.api.serializer.group import GroupCreateSerializer
from apps.accounts.models import AuthGroup


class GroupUpdateView(UpdateAPIView):
    serializer_class = GroupCreateSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        profile_name, profile = user.get_profile()

        # if not user.has_perm("auth.change_group"):
        #     return Response(
        #         {
        #             "success": False,
        #             "message": "You don't have permission update this Group",
        #         },
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        group_id = request.data.get("group_id")
        auth_group = get_object_or_404(AuthGroup, pk=group_id)
        group = get_object_or_404(Group, name=auth_group.name)

        group_name = request.data.get("name")
        group_description = request.data.get("description")
        group_permissions = request.data.get("permissions")

        if not group_name:
            return Response(
                {"message": "A name is required for each room", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not group_permissions or not group_permissions[0]:
            return Response(
                {"message": "At least on permission is required", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update group and auth_group details
        Group.objects.filter(pk=group.pk).update(name=group_name)
        auth_group.name = group.name
        auth_group.description = group_description or ""
        auth_group.save()

        perms_to_add = Permission.objects.filter(pk__in=group_permissions)
        group.permissions.set(perms_to_add)

        return Response(
            {
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
