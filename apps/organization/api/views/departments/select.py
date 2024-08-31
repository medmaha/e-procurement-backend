from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Department


class DepartmentSelectionView(ListAPIView):
    def get_queryset(self, query_params: dict):
        #
        queryset = Department.objects.filter().values("id", "name")
        return queryset

    def list(self, request, *args, **kwargs):
        profile_name, profile = request.user.get_profile()
        queryset = self.get_queryset(request.query_params)
        return Response(
            {"data": queryset},
            status=status.HTTP_200_OK,
        )
