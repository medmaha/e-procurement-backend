import random
from django.db import transaction
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Unit
from apps.organization.api.serializers.unit import UnitUpdateSerializer
from apps.accounts.models import Account


class UnitsUpdateView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        unit_id = request.data.get("obj_id")
        unit = Unit.objects.filter(id=unit_id).first()
        if not unit:
            return Response(
                {"success": False, "message": "Unit not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if "disable" in request.data:
            unit.disabled = True
            unit.save()
            return Response(
                {
                    "message": "Unit disabled",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        if "enable" in request.data:
            unit.disabled = False
            unit.save()
            return Response(
                {
                    "message": "Unit enabled successfully",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )

        serializer = UnitUpdateSerializer(
            instance=unit, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            print(serializer.validated_data)
            with transaction.atomic():
                unit: Unit = serializer.save()  # type: ignore
                return Response(
                    {
                        "message": 'Unit "%s" updated successfully' % unit.name,
                        "id": unit.pk,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"success": False, "message": get_clear_error_message(serializer.errors)},
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
