from functools import partial
from django.db import transaction

from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import Account
from apps.vendors.models import Vendor, ContactPerson, Certificate
from apps.accounts.api.views.account.login import populate_token

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import serializers

import os

from apps.core.models import Address
from apps.core.utilities.errors import get_serializer_error_message


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = [
            "active",
            "verified",
            "user_account",
            "contact_person",
            "certificates",
        ]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "avatar",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "middle_name",
        ]


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        exclude = [
            "verified",
            "date_achieved",
        ]


class CertificateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            "file",
        ]

    def save(self):
        pass


class VendorSignupView(CreateAPIView):
    permission_classes = []
    authentication_classes = []

    address = None

    def handle_certificates(self, request):
        vat_certificate = (
            request.data.get("vat_certificate")
            if "vat_certificate" in request.data
            else None
        )
        tin_certificate = (
            request.data.get("tin_certificate")
            if "tin_certificate" in request.data
            else None
        )
        license_certificate = (
            request.data.get("registration_certificate")
            if "registration_certificate" in request.data
            else None
        )

        data = (
            (vat_certificate, "VAT Certificate"),
            (tin_certificate, "TIN Certificate"),
            (license_certificate, "License Certificate"),
        )
        certificates = []
        for cert in data:
            file, name = cert
            __serializer = CertificateFileSerializer(data={"file": file})
            if not file or not __serializer.is_valid():
                return "Please provide a valid %s file" % name
            c = {}
            c["file"] = file
            c["name"] = name
            c["type"] = "-"
            c["achieved_from"] = "N/A"
            certificates.append(c)
        serializer = CertificateSerializer(data=certificates, many=True)
        return serializer

    def get_file_extension(self, file) -> str:
        file_name, file_extension = os.path.splitext(file.name)
        return file_extension

    def handle_contact_details(self, request):
        first_name = (
            request.data.get("c_first_name") if "c_first_name" in request.data else None
        )
        last_name = (
            request.data.get("c_last_name") if "c_last_name" in request.data else None
        )

        email = request.data.get("c_email") if "c_email" in request.data else None
        if ContactPerson.objects.filter(email=email).exists():
            return "A vendor contact with this email already exists."

        phone_number = (
            request.data.get("c_phone_number")
            if "c_phone_number" in request.data
            else None
        )
        if ContactPerson.objects.filter(phone_number=phone_number).count() > 1:
            return "This phone has already been registered"

        if not first_name or not last_name or not email or not phone_number:
            return "Invalid data for contact person. Missing field"

        town = request.data.get("c_town") if "c_town" in request.data else None
        if not town or len(town) < 4:
            return "Address town must be specified"

        country = request.data.get("c_country") if "c_country" in request.data else None
        if not country or len(country) < 4:
            return "Country for contact person is required"

        address = Address()
        address.town = town
        address.country = country
        address.region = request.data.get("c_region")
        address.district = request.data.get("c_district")
        self.address = address

        cp = ContactPerson()
        cp.first_name = first_name
        cp.last_name = last_name
        cp.email = email
        cp.address = address
        cp.phone_number = phone_number
        return cp

    def handle_user_details(self, request):
        first_name = (
            request.data.get("u_first_name") if "u_first_name" in request.data else None
        )
        middle_name = (
            request.data.get("u_middle_name")
            if "u_middle_name" in request.data
            else None
        )
        last_name = (
            request.data.get("u_last_name") if "u_last_name" in request.data else None
        )

        email = request.data.get("u_email") if "u_email" in request.data else None
        if Account.objects.filter(email=email).exists():
            return "A user with this email already exists."

        middle_name = (
            request.data.get("u_middle_name")
            if "u_middle_name" in request.data
            else None
        )
        phone_number = (
            request.data.get("u_phone_number")
            if "u_phone_number" in request.data
            else None
        )
        avatar = request.data.get("u_avatar") if "u_avatar" in request.data else None

        if not first_name or not last_name or not email:
            return "Invalid data for contact person. Missing field"
        password_1 = (
            request.data.get("u_password") if "u_password" in request.data else None
        )
        password_2 = (
            request.data.get("u_confirm_password")
            if "u_confirm_password" in request.data
            else None
        )
        if not password_1:
            return "Password is required for your account"

        if password_2 != password_1:
            return "Your password's do not match"

        u = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email,
            "avatar": avatar,
            "password": password_1,
        }

        return u

    def create(self, request):

        certificates_data = self.handle_certificates(request)  # type: ignore

        if isinstance(certificates_data, str):
            return Response(
                {"message": certificates_data},
                status=status.HTTP_400_BAD_REQUEST,
            )
        contact_data = self.handle_contact_details(request)
        if isinstance(contact_data, str):
            return Response(
                {"message": contact_data},
                status=status.HTTP_400_BAD_REQUEST,
            )
        account_data = self.handle_user_details(request)
        if isinstance(account_data, str):
            return Response(
                {"message": account_data},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vendor_serializer = VendorSerializer(data=request.data)
        account_serializer = AccountSerializer(data=account_data)

        # #
        __serializer = None
        if not certificates_data.is_valid():
            __serializer = certificates_data
        elif vendor_serializer.is_valid():
            if account_serializer.is_valid():
                committed = False
                with transaction.atomic():
                    if self.address:
                        self.address.save()
                    contact_data.save()

                    # FIXME: User profile image and vendor files are not being save to the correct directory
                    user_account: Account = account_serializer.save(is_superuser=False, is_staff=False, is_active=True)  # type: ignore
                    user_account.set_password(request.data.get("u_password"))  # type: ignore
                    user_account.save()
                    vendor: Vendor = vendor_serializer.save(address=self.address, contact_person=contact_data, user_account=user_account)  # type: ignore
                    certificates = certificates_data.save(vendor=vendor)
                    vendor.certificates.set(certificates)
                    committed = vendor.certificates.count() > 1

                transaction.on_commit(partial(self.mail_welcome_vendor, vendor))
                if committed:
                    return Response(
                        {
                            "info": "⚠️ Verify your email address and activate your account, to complete the registration process.",
                            "message": "Your success completed the initial process 👍",
                            "tokens": get_tokens_for_user(user_account),
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"message": "Oops! Something went wrong. Please try again."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            __serializer = account_serializer
        __serializer = vendor_serializer

        err_message = get_serializer_error_message(__serializer)

        return Response({"message": err_message}, status=status.HTTP_400_BAD_REQUEST)

    def mail_welcome_vendor(self, vendor: Vendor):
        pass


def get_tokens_for_user(user: Account):
    refresh = RefreshToken.for_user(user)
    token = populate_token(user, refresh)
    return {
        "refresh": str(refresh),
        "access": str(token.access_token),  # type: ignore
    }
