from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from apps.procurement.models import Requisition
from apps.procurement.api.serializers.requisition import (
    RequisitionRetrieveSerializer,
)
from apps.core.utilities.generators import revert_unique_id


class RequisitionRetrieveView(RetrieveAPIView):
    serializer_class = RequisitionRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        _id = revert_unique_id("R", slug or "0")
        print(slug)
        print(_id)
        instance = get_object_or_404(Requisition, pk=_id)
        serializer = self.get_serializer(
            instance=instance, context={"request": request}
        )
        auth_perms = {
            "create": request.user.has_perm("procurement.add_requisition"),
            "read": request.user.has_perm("procurement.view_requisition"),
            "update": request.user.has_perm("procurement.change_requisition"),
            "delete": request.user.has_perm("procurement.delete_requisition"),
        }

        data = {"data": serializer.data, "auth_perms": auth_perms}

        return Response(data, status=status.HTTP_200_OK)
