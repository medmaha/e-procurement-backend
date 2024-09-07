from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import Account
from rest_framework.response import Response

from backend.apps.organization.models.unit import Unit


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: Account):
        token = populate_token(user, super().get_token(user))
        return token


class LoginAPIView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code != 200:
            response = Response(
                {"error": "Oops!Invalid credentials"}, status=response.status_code
            )

        return super().finalize_response(request, response, *args, **kwargs)


def populate_token(user: Account, token):
    profile_type, profile = user.get_profile()

    payload = {}
    payload["name"] = user.full_name
    payload["profile_id"] = profile.pk
    payload["profile_type"] = profile_type

    payload["meta"] = {}

    if profile_type == "Vendor":
        registration = profile.vendorregistration_set.select_related().first()
        vendor = {
            "id": profile.pk,
            "name": profile.organization_name,
            "industry": profile.industry,
            "is_validated": registration.is_validated,
            "activation_status": registration.status,
        }
        payload["meta"]["vendor"] = vendor

    elif profile_type == "Staff":
        unit: Unit = profile.unit
        department = unit.department
        staff = {
            "id": profile.pk,
            "name": user.full_name,
            "unit": {
                "slug": unit.slug,
                "name": unit.name,
            },
            "department": {
                "slug": department.slug,
                "name": department.name,
            },
            "company": {
                "name": department.company.name,
                "slug": department.company.slug,
            },
            "is_activated": not profile.disabled,
            "created_date": profile.created_date,
        }
        payload["meta"]["staff"] = staff

    token["user"] = payload
    return token
