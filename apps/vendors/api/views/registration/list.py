import threading
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.vendors.models import VendorRegistration
from apps.vendors.api.serializers.registration import (
    VendorRegistrationListSerializer,
)


class RegistrationListView(ListAPIView):
    serializer_class = VendorRegistrationListSerializer

    def list(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()
        many = True
        query = {}
        if profile_type == "Vendor":
            many = False
            query.update({"vendor": profile})

        queryset = VendorRegistration.objects.filter(**query)
        qs = queryset if many else queryset.first()

        serializer = self.get_serializer(qs, many=many, context={"request": request})

        auth_perms = {
            "create": request.user.has_perm("vendors.add_vendorregistration"),
            "read": request.user.has_perm("vendors.view_vendorregistration"),
            "update": request.user.has_perm("vendors.change_vendorregistration"),
            "delete": request.user.has_perm("vendors.delete_vendorregistration"),
        }
        return Response({"data": serializer.data, "auth_perms": auth_perms})
