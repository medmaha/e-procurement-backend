from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Staff
from apps.organization.api.serializers.staff import (
    StaffSelectionSerializer,
)
from apps.accounts.models import Account


class StaffSelectionView(ListAPIView):
    serializer_class = StaffSelectionSerializer

    def get_queryset(self):
        queryset = Staff.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
