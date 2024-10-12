import re
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.vendors.models import Certificate, Vendor
from rest_framework import serializers


class CertificateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"


class CertificationUpdateView(UpdateAPIView):
    serializer_class = CertificateUpdateSerializer

    def update(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()  # type: ignore

        if profile_type != "Vendor":
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # remove the file from the request to avoid setting the file to none
        if "file" in request.data:
            _file = request.data["file"]
            if not _file or str(_file) == "undefined":
                del request.data["file"]

        instance = get_object_or_404(Certificate, pk=request.data.get("certificate_id"))

        serializer = self.get_serializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Certificate updated successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "The data you provided is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )
