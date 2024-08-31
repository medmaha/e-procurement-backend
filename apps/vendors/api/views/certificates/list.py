from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from apps.vendors.models import Certificate
from apps.vendors.api.serializers.certificates import CertificateListSerializer


class CertificationListView(ListAPIView):
    serializer_class = CertificateListSerializer

    def get_queryset(self, profile_type, profile):
        if profile_type == "Vendor":
            return profile.certificates.filter()
        return Certificate.objects.filter()

    def list(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()  # type: ignore
        queryset = self.get_queryset(profile_type, profile)
        serializer = self.get_serializer(
            self.filter_queryset(queryset), many=True, context={"request": request}
        )
        auth_perms = {
            "update": request.user.has_perm("vendors.change_vendorregistration"),
        }
        return Response({"data": serializer.data, "auth_perms": auth_perms})
