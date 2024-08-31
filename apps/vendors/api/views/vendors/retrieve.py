import threading
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.vendors.models import Vendor, Certificate, ContactPerson
from apps.accounts.models import Account


class VendorCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "name"]


class VendorUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email"]


class VendorContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ["id", "email"]


class VendorSerializer(serializers.ModelSerializer):
    user_account = VendorUserAccountSerializer()
    contact_person = VendorContactPersonSerializer()
    certificates = VendorCertificateSerializer(many=True)

    class Meta:
        model = Vendor
        exclude = []


class VendorRetrieveView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()
        query = None
        auth_perms = {}
        if profile_type == "Vendor":
            auth_perms = {
                "update": True,
            }
            query = {"pk": profile.id}

        elif profile_type == "Staff":
            object_id = request.query_params.get("oid")
            query = {"pk": object_id}
        if not query:
            return Response(
                {"message": "You are not a vendor"}, status=status.HTTP_400_BAD_REQUEST
            )
        instance = get_object_or_404(Vendor, **query)
        serializer = VendorSerializer(instance=instance, context={"request": request})

        return Response({"data": serializer.data, "auth_perms": auth_perms})


class VendorDetailsView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()
        # TODO: Do some Authorization
        slug = kwargs.get("slug", "0")
        instance = get_object_or_404(Vendor, pk=slug)
        auth_perms = {}
        serializer = VendorSerializer(instance=instance, context={"request": request})

        return Response({"data": serializer.data, "auth_perms": auth_perms})
