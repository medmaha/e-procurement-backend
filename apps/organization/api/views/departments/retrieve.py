from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Department
from apps.organization.api.serializers.department import DepartmentRetrieveSerializer
from apps.accounts.models import Account


class DepartmentRetrieveView(RetrieveAPIView):
    serializer_class = DepartmentRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        department = Department.objects.filter(id=kwargs.get("id")).first()

        if not department:
            return Response(
                {"success": False, "message": "Department not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(department)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )
