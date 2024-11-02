from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.vendors.models import ContactPerson
from apps.vendors.api.serializers.contact_person import ContactPersonRetrieveSerializer
from apps.core.utilities.generators import revert_generated_unique_id


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = [
            "first_name",
            "last_name",
            "email",
            "verified",
            "phone_number",
            "last_modified",
        ]

    def to_representation(self, instance: ContactPerson):
        data = super().to_representation(instance)

        if instance.address:
            data["address"] = {
                "id": instance.address.pk,
                "string": instance.address.to_string,
            }

        return data

    def get_address(self, instance: ContactPerson):
        return instance.address.to_string if instance.address else None


class ContactPersonRetrieveView(RetrieveAPIView):
    serializer_class = ContactPersonSerializer

    def get_queryset(self, request, profile_type, profile):
        if profile_type == "Vendor":
            return ContactPerson.objects.filter(vendors=profile).first()

        else:
            return ContactPerson.objects.filter(
                vendor_id=request.query_params.get("vendor", "0")
            ).first()

    def retrieve(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()
        queryset = self.get_queryset(request, profile_type, profile)
        if queryset:
            serializer = self.get_serializer(instance=queryset, many=False)
            return Response({"data": serializer.data})

        return Response({"message": "Contact person couldn't be found"})


class ContactPersonRetrieveDetailsView(RetrieveAPIView):
    serializer_class = ContactPersonRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()

        slug = kwargs.get("slug") or "0"
        _id = revert_generated_unique_id("", slug)
        instance = get_object_or_404(ContactPerson, pk=_id)
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data})
