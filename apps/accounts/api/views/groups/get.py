from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.accounts.models import AuthGroup
from apps.accounts.serializer.group import (
    GroupRetrieveSerializer,
)


class GroupGetAPIView(RetrieveAPIView):
    serializer_class = GroupRetrieveSerializer

    def get_queryset(self, group_id, company_id):
        try:
            return AuthGroup.objects.get(pk=group_id, company_id=company_id)
        except:
            return None

    def retrieve(self, request, group_id, *args, **kwargs):

        profile_type, profile = request.user.get_profile()

        if not profile_type.lower() == "staff":
            return Response(
                {"error": "Permission denied!"},
                status=403,
            )

        queryset = self.get_queryset(group_id, str(profile.department.company.pk))

        if not queryset:
            return Response(
                {"error": "Group not found"},
                status=404,
            )

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
