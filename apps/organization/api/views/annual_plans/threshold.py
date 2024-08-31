from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models.procurement_plan import Threshold

from apps.accounts.models import Account


class ProcurementMethodThresholdView(ListAPIView):
    def get_queryset(self):
        queryset = Threshold.objects.filter().values(
            "id", "min_amount", "max_amount", "description", "procurement_method"
        )
        return queryset

    def list(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        queryset = self.get_queryset()

        auth_perms = {
            "create": request.user.has_perm("organization.add_threshold"),
            "read": request.user.has_perm("organization.view_threshold"),
            "update": request.user.has_perm("organization.change_threshold"),
            "delete": request.user.has_perm("organization.delete_threshold"),
        }

        return Response(
            {"data": queryset, "auth_perms": auth_perms}, status=status.HTTP_200_OK
        )
