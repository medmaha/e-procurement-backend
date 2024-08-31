from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import Account
from apps.vendors.models.vendor import Vendor


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: Account):
        token = populate_token(user, super().get_token(user))
        return token


class LoginTokensObtainView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        # for v in Vendor.objects.all():
        #     v.user_account.set_password("prc@2k2*")
        #     v.user_account.save()

        # for acc in Account.objects.all():
        # acc.set_password("prc@2k2*")

        if response.status_code > 201:
            if request.method == "POST":
                response.data.update({"detail": "Oops! your credentials are invalid"})
        return super().finalize_response(request, response, *args, **kwargs)


def populate_token(user: Account, token):
    profile_type, profile = user.get_profile()

    payload = {}
    payload["name"] = user.full_name
    payload["profile_id"] = profile.pk
    payload["profile_type"] = profile_type

    payload["meta"] = {}
    payload["meta"]["id"] = user.pk

    if profile_type == "Vendor":
        registration = profile.vendorregistration_set.first()
        vendor = {
            "id": profile.pk,
            "name": profile.organization_name,
            "industry": profile.industry,
            "is_validated": registration.is_validated,
            "activation_status": registration.status,
        }
        payload["meta"]["vendor"] = vendor

    elif profile_type == "Staff":
        unit = profile.unit
        department = unit.department
        staff = {
            "id": profile.pk,
            "unit": unit.name,
            "department": department.name,
            "is_activated": not profile.disabled,
        }
        payload["meta"]["staff"] = staff

    token["user"] = payload
    return token
