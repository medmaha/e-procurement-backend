from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import Account
from rest_framework.response import Response

from apps.organization.models.unit import Unit


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: Account):
        _token = super().get_token(user)
        token = populate_token(user, _token)
        return token


class LoginAPIView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code != 200:
            response = Response(
                {"error": "Oops! Invalid credentials"}, status=response.status_code
            )
        return super().finalize_response(request, response, *args, **kwargs)


def populate_token(user: Account, token):
    profile_type, profile = user.get_profile()

    user_id = str(user.id)

    payload = {}
    payload["meta"] = {}
    payload["id"] = user_id
    payload["name"] = user.full_name

    if not profile:
        token["user_id"] = user_id
        token["user"] = payload

        return token

    payload["profile_id"] = str(profile.id)
    payload["profile_type"] = profile_type

    if profile_type == "Vendor":
        vendor = {
            "id": str(profile.id),
            "company": {
                "name": profile.company.name,
                "slug": profile.company.slug,
            },
            "created_date": str(profile.created_date),
        }
        payload["meta"]["vendor"] = vendor

    elif profile_type == "Staff":
        unit: Unit = profile.unit
        department = unit.department
        staff = {
            "id": str(profile.id),
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
            "created_date": str(profile.created_date),
        }
        payload["meta"]["staff"] = staff

    token["user"] = payload
    return token
