from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Staff
from apps.organization.api.serializers.staff import (
    StaffRetrieveSerializer,
    StaffUpdateRetrieveSerializer,
)

from apps.accounts.models import Account
from apps.core.utilities.generators import revert_generated_unique_id


class StaffRetrieveView(RetrieveAPIView):
    serializer_class = StaffRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        slug = revert_generated_unique_id("EM", kwargs.get("id") or "0")
        staff = get_object_or_404(Staff, pk=slug)

        if not staff:
            return Response(
                {"success": False, "message": "Staff not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(staff)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )


class StaffUpdateRetrieveView(RetrieveAPIView):
    serializer_class = StaffUpdateRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, id=kwargs.get("id"))
        serializer = self.get_serializer(instance=staff, context={"request": request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
