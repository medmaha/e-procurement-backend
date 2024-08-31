from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.core.processors.temp_db import EmailVerificationDB
from apps.core.emails.email_verification import send_verification_code
from apps.vendors.models.contact_person import ContactPerson


class ContactPersonVerifyView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        if profile_type != "Vendor":
            return Response(
                {"message": "Permission denied, You are not a vendor"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        contact_person: ContactPerson = vendor.contact_person

        if contact_person.verified:
            return Response(
                {"message": "Contact information already verified"},
            )

        [code, expiration, delete_record] = EmailVerificationDB.generate_code(
            contact_person.email
        )
        send_verification_code(
            contact_person,  # type: ignore
            code,
            expiration,
        )
        # delete_record()
        return Response(
            {"message": "Verification code is being sent to your email."},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()

        if profile_type != "Vendor":
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contact_person = vendor.contact_person

        if contact_person.verified:
            return Response(
                {"message": "Contact information already verified"},
            )

        code_matches = EmailVerificationDB.verify_code(
            contact_person.email,
            request.data.get("code", "-0-0-"),
        )
        if not code_matches:
            return Response(
                {"message": "Invalid verification code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contact_person.verified = True
        contact_person.save()
        EmailVerificationDB.delete(contact_person.email)
        return Response(
            {"message": "Contact information verified successfully"},
        )
