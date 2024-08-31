import random
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Unit
from apps.organization.api.serializers.unit import UnitCreateSerializer
from apps.accounts.models import Account


class UnitsCreateView(CreateAPIView):
    serializer_class = UnitCreateSerializer

    def create(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        serializer = self.get_serializer(data=request.data)

        print(request.data)
        if serializer.is_valid():
            existing_unit = Unit.objects.filter(
                name__iexact=serializer.validated_data.get("name")
            )
            if existing_unit:
                return Response(
                    {
                        "success": False,
                        "message": 'Unit "%s" already exists' % existing_unit.name,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {"message": "Unit created successfully", "success": True},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "message": get_clear_error_message(serializer.errors)},
            status=status.HTTP_400_BAD_REQUEST,
        )


def get_clear_error_message(serializer_errors):
    error_list = []
    if serializer_errors and isinstance(serializer_errors, dict):
        for field, errors in serializer_errors.items():
            if isinstance(errors, list):
                for error in errors:
                    if isinstance(error, str):
                        error_list.append(str(error))

    if error_list:
        return error_list[random.randrange(0, len(error_list))]
    return "Something went wrong"
