from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.vendors.models import Certificate
from apps.vendors.api.serializers.certificates import (
    CertificateRetrieveSerializer,
)
from apps.core.utilities.generators import revert_generated_unique_id


class CertificateRetrieveView(RetrieveAPIView):
    serializer_class = CertificateRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        _id = revert_generated_unique_id("", slug or "0")
        instance = get_object_or_404(Certificate, pk=_id)
        serializer = self.get_serializer(instance, context={"request": request})
        auth_perms = {
            "create": request.user.has_perm("vendors.add_certificate"),
            "read": request.user.has_perm("vendors.view_certificate"),
            "update": request.user.has_perm("vendors.change_certificate"),
            "delete": request.user.has_perm("vendors.delete_certificate"),
        }
        data = {"data": serializer.data, "auth_perms": auth_perms}
        return Response(data, status=status.HTTP_200_OK)
