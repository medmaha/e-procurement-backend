from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.procurement.models import RFQ
from apps.procurement.api.serializers.rfq import (
    RFQListSerializer,
)
from apps.core.utilities.generators import revert_unique_id
from apps.procurement.api.serializers.quotations import RFQItemsSerializer
from apps.organization.models.staff import Staff


class RfqRetrieveView(RetrieveAPIView):
    serializer_class = RFQListSerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        _id = revert_unique_id("RFQ", slug or "0")
        instance = get_object_or_404(RFQ, pk=_id)
        officer: Staff = instance.officer  # type: ignore
        if request.query_params.get("only") == "items":
            data = {
                "unique_id": instance.unique_id,
                "officer": {"id": officer.pk, "name": officer.name},
                "requisition": {"id": instance.requisition.pk, "unique_id": instance.requisition.unique_id},  # type: ignore
                "items": RFQItemsSerializer(instance.items, many=True).data,
            }
        else:
            data = self.get_serializer(instance, context={"request": request}).data
        auth_perms = {
            "read": request.user.has_perm("procurement.view_rfq"),
            "update": request.user.has_perm("procurement.change_rfq"),
        }
        data = {"data": data, "auth_perms": auth_perms}
        return Response(data, status=status.HTTP_200_OK)
