from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Subquery
from apps.accounts.api.serializer.permissions import PermissionSelectListSerializer


class PermissionSelectListView(ListAPIView):
    serializer_class = PermissionSelectListSerializer

    def get_queryset(self):
        apps = ["organization", "procurement", "vendors"]

        perms = Permission.objects.filter(
            Q(
                content_type__id__in=Subquery(
                    ContentType.objects.filter(app_label="accounts").values("id")
                )
            )
        ).exclude(codename__regex=r"(?i)(view|user|delete)")

        perms1 = Permission.objects.filter(
            Q(
                content_type__id__in=Subquery(
                    ContentType.objects.filter(app_label="organization").values("id")
                )
            )
        ).exclude(codename__regex=r"(?i)(view|delete_annual|planitem|threshold)")

        perms2 = Permission.objects.filter(
            Q(
                content_type__id__in=Subquery(
                    ContentType.objects.filter(app_label="procurement").values("id")
                )
            )
        ).exclude(
            codename__regex=r"(?i)(view|delete_annual|item|_requisitionapproval|threshold)"
        )

        # perms = perms.exclude(codename__icontains="delete_vendorreg")

        return perms | perms1 | perms2

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
