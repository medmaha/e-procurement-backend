from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Department
from apps.organization.api.serializers.department import DepartmentUpdateSerializer
from apps.accounts.models import Account
from apps.core.utilities.errors import get_serializer_error_message


class DepartmentUpdateView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        # TODO! Check user permissions

        department_id = request.data.get("obj_id")
        department = Department.objects.filter(id=department_id).first()
        if not department:
            return Response(
                {"success": False, "message": "Department not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if "disable" in request.data:
            department.disabled = True
            department.save()
            return Response(
                {
                    "id": department.pk,
                    "message": "Department disabled",
                },
                status=status.HTTP_200_OK,
            )
        if "enable" in request.data:
            department.disabled = False
            department.save()
            return Response(
                {
                    "id": department.pk,
                    "message": "Department enabled successfully",
                },
                status=status.HTTP_200_OK,
            )

        serializer = DepartmentUpdateSerializer(
            instance=department, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()  # type: ignore
            return Response(
                {
                    "message": "Department created successfully",
                    "id": department.pk,
                },
                status=status.HTTP_200_OK,
            )

        error_message = get_serializer_error_message(serializer)
        return Response(
            {"success": False, "message": error_message},
        )
