from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.vendors.models import VendorRegistration
from apps.vendors.api.serializers.registration import (
    VendorRegistrationRetrieveSerializer,
)
from apps.core.utilities.generators import revert_unique_id


class VendorRegistrationRetrieveView(RetrieveAPIView):
    serializer_class = VendorRegistrationRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        _id = revert_unique_id("RFQ", slug or "0")
        instance = get_object_or_404(VendorRegistration, pk=_id)
        serializer = self.get_serializer(instance, context={"request": request})
        auth_perms = {
            "create": request.user.has_perm("vendors.add_vendorregistration"),
            "read": request.user.has_perm("vendors.view_vendorregistration"),
            "update": request.user.has_perm("vendors.change_vendorregistration"),
            "delete": request.user.has_perm("vendors.delete_vendorregistration"),
        }
        data = {"data": serializer.data, "auth_perms": auth_perms}
        return Response(data, status=status.HTTP_200_OK)
