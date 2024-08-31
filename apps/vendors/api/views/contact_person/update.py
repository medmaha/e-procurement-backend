from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework import serializers
from apps.vendors.models import ContactPerson
from apps.core.utilities.errors import get_serializer_error_message


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]


class ContactPersonUpdateView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        if profile_type != "Vendor":
            return Response(
                {"message": "You are not a vendor"}, status=status.HTTP_400_BAD_REQUEST
            )

        instance: ContactPerson = vendor.contact_person
        serializer = ContactPersonSerializer(instance=instance, data=request.data)

        if serializer.is_valid():
            # toggle the verification when an email is updated
            verified = vendor.contact_person.verified
            new_email = request.data.get("email")

            if new_email and (new_email != instance.email):
                verified = False
            serializer.save(verified=verified)

            return Response(
                {"message": "Contact information updated successfully"},
                status=status.HTTP_200_OK,
            )

        err_message = get_serializer_error_message(serializer)
        return Response({"message": err_message}, status=status.HTTP_400_BAD_REQUEST)
