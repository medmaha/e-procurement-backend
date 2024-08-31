from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.vendors.models import Certificate
from apps.core.utilities.errors import get_serializer_error_message


class CertificationVerificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["verified"]


class CertificationVerificationUpdateView(UpdateAPIView):
    serializer_class = CertificationVerificationUpdateSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm("vendors.change_vendorregistration"):
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance = get_object_or_404(Certificate, pk=request.data.get("pk", 0))

        serializer = self.get_serializer(instance=instance, data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                # TODO: Log Entry
                serializer.save()
                return Response(
                    {"id": instance.pk, "message": "Registration updated successfully"}
                )

        return Response(
            {"message": get_serializer_error_message(serializer)},
            status=status.HTTP_400_BAD_REQUEST,
        )
