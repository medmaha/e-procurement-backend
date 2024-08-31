from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Department
from apps.organization.api.serializers.department import DepartmentCreateSerializer
from apps.accounts.models import Account


class DepartmentCreateView(CreateAPIView):
    serializer_class = DepartmentCreateSerializer

    def create(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            existing_department = Department.objects.filter(
                name__iexact=serializer.validated_data.get("name")
            )
            if existing_department:
                return Response(
                    {
                        "success": False,
                        "message": 'Department "%s" already exists'
                        % existing_department.name,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {"message": "Department created successfully", "success": True},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "The following errors occurred: \n"}
        )
