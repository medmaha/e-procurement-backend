from django.db import transaction
from django.contrib.auth.models import Group
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Staff
from apps.organization.api.serializers.staff import StaffCreateSerializer
from apps.accounts.models import Account
from apps.organization.models.unit import Unit
from apps.core.utilities.errors import get_serializer_error_message


class StaffCreateView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        # check if user has admin privilege to create the staff

        admin_privilege = user.has_perm("organization.add_staff")
        if profile_name != "Staff" or not admin_privilege:
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        group_ids = [i or 0 for i in request.data.get("group_ids", [])]
        groups = []
        if len(group_ids):
            try:
                groups = Group.objects.filter(pk__in=group_ids)
            except:
                return Response(
                    {
                        "success": False,
                        "message": "Error! One or more groups not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = StaffCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            with transaction.atomic():
                staff: Staff = serializer.save()  # type: ignore
                if len(groups):
                    staff.user_account.groups.add(*groups)
                return Response(
                    {"message": "Staff created successfully", "success": True},
                    status=status.HTTP_201_CREATED,
                )

            # TODO: email staff with login credentials
            # transaction.on_commit
        error_message = get_serializer_error_message(serializer)
        return Response(
            {"success": False, "message": error_message},
            status=status.HTTP_400_BAD_REQUEST,
        )
