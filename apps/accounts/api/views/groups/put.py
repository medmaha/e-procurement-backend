from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.accounts.serializer.group import (
    GroupUpdateSerializer,
    GroupRetrieveSerializer,
)
from apps.accounts.models import AuthGroup
from apps.core.utilities.errors import get_serializer_error_message


class GroupUpdateAPIView(UpdateAPIView):
    """
    Update a group
    """

    serializer_class = GroupUpdateSerializer

    def get_queryset(self, group_id: str, author_id: str):
        try:
            return AuthGroup.objects.get(
                pk=group_id, editable=True, authored_by=author_id
            )
        except:
            return None

    def update(self, request, group_id, *args, **kwargs):
        """
        Update a group, it's permissions and parent group
        """
        user = request.user
        profile_name, profile = user.get_profile()

        # Check permission
        if profile_name.lower() != "staff":
            return Response(
                {"error": "Permission denied!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if user has permission to update the group
        # if not user.has_perm("account.change_authgroup"):
        #     return Response(
        #         {
        #             "error": "You don't have permission to update this Group",
        #         },
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        with transaction.atomic():
            # get the group name from request data
            group_name = request.data.get("name")

            # get the permissions from request data
            group_permissions = request.data.get("permissions")

            # Check if permissions is valid
            if group_permissions and not isinstance(group_permissions, list):
                return Response(
                    {"error": "Permissions must be a list"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Reconstruct the parent group name
            parent_group_name = f"{group_name} | {str(profile.pk)}"

            # If a group with this name already exists, return 409 Conflict
            already_exists = lambda: Response(
                {"error": "Group already exists"},
                status=status.HTTP_409_CONFLICT,
            )

            # Check if group name already exists
            _group_exists = Group.objects.filter(name__iexact=parent_group_name.lower())

            if _group_exists.exists():
                # return 409 Conflict
                return already_exists()

            # Check if auth group already exists
            _auth_group_exists = AuthGroup.objects.filter(
                name__iexact=parent_group_name.lower()
            )

            if _auth_group_exists.exists():
                # return 409 Conflict
                return already_exists()

            # get the auth group object
            # auth_group = self.get_queryset(group_id, str(profile.pk))
            auth_group = get_object_or_404(AuthGroup, pk=group_id)

            # Check if group is editable
            if auth_group.editable is False:
                return Response(
                    {"error": "This group is not mutable"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # set the group name
            group_name = group_name or auth_group.name

            # Check if name is valid
            if not group_name:
                return Response(
                    {"error": "A name is required for each room"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Make sure the user has permission to update the group
            if auth_group.authored_by != str(profile.pk):
                return Response(
                    {"error": "You don't have permission to update this Group"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Get the current parent group
            group = Group.objects.filter(pk=auth_group.group_id).first()
            if not group:
                # Create a new group with the parent group name
                group, _ = Group.objects.get_or_create(name=parent_group_name)
                auth_group.group_id = group.pk  # Update the auth-group group_id
                auth_group.save()

            serializer = self.get_serializer(auth_group, data=request.data)

            # Check if serializer is valid
            if not serializer.is_valid():
                return Response(
                    {
                        "error": get_serializer_error_message(
                            serializer, "Invalid data provided"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Reconstruct parent group name
            parent_group_name = f"{group_name} | {str(auth_group.company_id)}"

            # Update the parent group name
            Group.objects.filter(pk=group.pk).update(name=parent_group_name)

            # Only update permissions if group_permissions is not empty
            if group_permissions and len(group_permissions) > 0:
                perms_to_add = Permission.objects.filter(pk__in=group_permissions)
                # Reset permissions for group
                group.permissions.set(perms_to_add)

            # Save the updated auth-group
            result = serializer.save()
            result_serializer = GroupRetrieveSerializer(result)

            return Response(
                result_serializer.data,
                status=status.HTTP_200_OK,
            )
