from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.vendors.models import Certificate
from rest_framework import serializers

from apps.core.utilities.errors import get_serializer_error_message


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        exclude = ["vendor", "type"]


class CertificationCreateView(CreateAPIView):
    serializer_class = CertificateSerializer

    def create(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()  # type: ignore

        if profile_type != "Vendor":
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            with transaction.atomic():
                file = serializer.validated_data.get("file")
                if not file:
                    return Response(
                        {"message": "You need to provide a certification file"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                vendor.certificates.add(
                    serializer.save(vendor=vendor, type=file.content_type.split("/")[1])
                )
                return Response(
                    {"message": "Certificate added successfully"},
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {"message": get_serializer_error_message(serializer)},
            status=status.HTTP_400_BAD_REQUEST,
        )
