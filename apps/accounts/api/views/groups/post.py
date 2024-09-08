from django.db import transaction
from django.contrib.auth.models import Group, Permission

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.accounts.serializer.group import (
    GroupCreateSerializer,
    GroupRetrieveSerializer,
)
from apps.core.utilities.errors import get_serializer_error_message


class GroupCreateAPIView(CreateAPIView):
    serializer_class = GroupCreateSerializer

    def create(self, request, *args, **kwargs):
        # TODO: Check if the user has permission here

        profile_type, profile = request.user.get_profile()

        if profile_type.lower() != "staff":
            return Response(
                {"error": "Only Staff can create groups"},
                status=status.HTTP_403_FORBIDDEN,
            )

        company = profile.department.company

        # Extract permissions from request data
        perms = request.data.pop("permissions", [])

        if not perms or not perms[0]:
            return Response(
                {"error": "Please provide at least on permissions"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group_name = request.data.get("name")
        group_description = request.data.get("description")

        parent_group_name = f"{group_name} | {str(company.id)}"

        if not group_name:
            return Response(
                {"error": "A name is required for each group"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not group_description:
            return Response(
                {
                    "error": "A description is required for each group",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        group_exist = Group.objects.filter(name__iexact=parent_group_name.lower())

        if group_exist.exists():
            return Response(
                {
                    "error": "A group with this name already exists",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        permissions = Permission.objects.filter(pk__in=perms)

        if not permissions.exists():
            return Response(
                {
                    "error": "Invalid permissions provided",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            parent_group = Group.objects.create(name=parent_group_name)
            data = {
                "company_id": str(company.pk),
                "authored_by": str(profile.pk),
                "group_id": str(parent_group.pk),
                "editable": True,
                "name": group_name,
                "description": group_description,
            }

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                auth_group = serializer.save()

                parent_group.permissions.set(permissions)

                results_serializer = GroupRetrieveSerializer(instance=auth_group)

                return Response(
                    results_serializer.data,
                    status=status.HTTP_201_CREATED,
                )

            error_message = get_serializer_error_message(
                serializer, "Invalid data provided"
            )
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
