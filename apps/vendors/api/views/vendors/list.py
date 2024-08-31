from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView

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

    class Meta:
        model = Vendor
        fields = [
            "id",
            "organization_name",
            "user_account",
            "contact_person",
            "verified",
            "unique_id",
            "created_date",
            "last_modified",
        ]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if instance.contact_person:
    #         if instance.contact_person.verified:
    #             instance.verified = True
    #             instance.save()
    #     return data


class VendorListView(ListAPIView):
    def get_queryset(self):
        queryset = Vendor.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        # queryset = get_object_or_404(ContactPerson, vendor=vendor)

        # TODO: Check the user's permissions
        if profile_type != "Staff":
            return Response(
                {"message": "You are not a vendor"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VendorSerializer(
            instance=self.get_queryset(), context={"request": request}, many=True
        )
        return Response({"data": serializer.data})
