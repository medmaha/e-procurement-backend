from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Unit
from apps.organization.api.serializers.unit import (
    UnitListSerializer,
    UnitSelectionSerializer,
)
from apps.accounts.models import Account


class UnitSelectionView(ListAPIView):
    serializer_class = UnitSelectionSerializer

    def get_queryset(self):
        queryset = Unit.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
