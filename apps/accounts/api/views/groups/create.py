from django.db import transaction
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.accounts.api.serializer.group import GroupCreateSerializer
from apps.accounts.models import AuthGroup


class GroupCreateView(CreateAPIView):
    serializer_class = GroupCreateSerializer

    def create(self, request, *args, **kwargs):
        # TODO: Check if the user has permission here

        # Extract permissions from request data
        perms = request.data.get("permissions", [])

        if not perms or not perms[0]:
            return Response(
                {"success": False, "message": "Please provide at least on permissions"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data.update({"editable": True})

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            group_name = request.data.get("name")
            group_description = request.data.get("description", "")

            if not group_name:
                return Response(
                    {"message": "A name is required for each group", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not group_description:
                return Response(
                    {
                        "message": "A description is required for each group",
                        "success": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            permissions = Permission.objects.filter(pk__in=perms)
            created = Group.objects.filter(name__iexact=group_name).exists()
            if created:
                return Response(
                    {
                        "success": False,
                        "message": "A group with this name already exists",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            with transaction.atomic():
                group = Group.objects.create(name=group_name)
                # Create AuthGroup // AuthGroup is automatically when a new Django Group is created
                AuthGroup.objects.filter(group_id=group.pk).update(
                    editable=True,
                    description=group_description,
                    authored_by=str(request.user.email),
                )
                group.permissions.set(permissions)
                return Response(
                    {"message": "Auth group was created successfully"},
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {
                "success": False,
                "message": "Invalid data provided",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
