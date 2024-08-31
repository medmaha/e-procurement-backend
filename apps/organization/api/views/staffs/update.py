import random
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Staff
from apps.organization.api.serializers.staff import (
    # StaffAdminUpdateSerializer,
    AdminStaffUpdateSerializer,
    StaffUpdateSerializer,
)
from apps.accounts.models import Account
from apps.core.utilities.errors import get_serializer_error_message


class StaffUpdateView(UpdateAPIView):
    serializer_class = StaffUpdateSerializer

    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        if profile_name != "Staff":
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        staff_id = request.data.get("obj_id")
        staff = get_object_or_404(Staff, id=staff_id)

        # check if user has admin privilege to update the staff
        admin_privilege = user.has_perm("organization.add_staff")
        if admin_privilege:
            with transaction.atomic():
                if "disable" in request.data or "enable" in request.data:
                    is_enabled = request.data.get("enable") is not None
                    staff.disabled = not is_enabled
                    staff.save()
                    return Response(
                        {
                            "message": "Staff %s successfully" % "enabled"
                            if is_enabled
                            else "disabled",
                        },
                        status=status.HTTP_200_OK,
                    )
                if "group_ids" in request.data:
                    try:
                        groups = Group.objects.filter(
                            Q(pk__in=request.data["group_ids"])
                        ).distinct()

                        # a user IT-Admin permissions
                        if staff == profile:
                            groups = groups = Group.objects.filter(
                                Q(pk__in=[1, 8]) | Q(pk__in=request.data["group_ids"])
                            ).distinct()
                            staff.user_account.groups.set(groups)
                        else:
                            staff.user_account.groups.set(groups)
                    except Exception:
                        return Response(
                            {
                                "message": "Group not found",
                            },
                            status=status.HTTP_404_NOT_FOUND,
                        )

                serializer = AdminStaffUpdateSerializer(
                    instance=staff, data=request.data, context={"request": request}
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "message": "Staff updated successfully",
                            "id": staff.pk,
                        },
                        status=status.HTTP_200_OK,
                    )
                error_message = get_serializer_error_message(serializer)
                print(error_message)
                return Response(
                    {"message": error_message},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Otherwise the staff can only update his own profile
        elif staff == profile:
            serializer = StaffUpdateSerializer(
                instance=staff, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Staff updated successfully",
                        "id": staff.pk,
                    },
                    status=status.HTTP_200_OK,
                )
            error_message = get_serializer_error_message(serializer)
            print(error_message)
            return Response(
                {"message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Error! The staff could not be updated"},
            status=status.HTTP_400_BAD_REQUEST,
        )
