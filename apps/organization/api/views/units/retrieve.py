from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Unit
from apps.organization.api.serializers.unit import (
    UnitRetrieveSerializer,
    UnitRetrieveUpdateSerializer,
)
from apps.accounts.models import Account


class UnitsRetrieveView(RetrieveAPIView):
    serializer_class = UnitRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        unit = Unit.objects.filter(id=kwargs.get("id")).first()

        if not unit:
            return Response(
                {"success": False, "message": "Unit not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(unit)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )


class UnitsRetrieveUpdateView(RetrieveAPIView):
    serializer_class = UnitRetrieveUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        unit = Unit.objects.filter(id=kwargs.get("id")).first()

        if not unit:
            return Response(
                {"success": False, "message": "Unit not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(unit)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )
