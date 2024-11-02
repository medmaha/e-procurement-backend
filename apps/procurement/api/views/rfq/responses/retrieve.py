from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.procurement.api.serializers.quotations import (
    RFQResponseRetrieveSerializer,
)
from apps.vendors.models.rfq_response import RFQResponse
from apps.core.utilities.generators import revert_generated_unique_id
from apps.procurement.models.rfq_contract import RFQContract


class QuotationRespondRetrieveView(RetrieveAPIView):
    serializer_class = RFQResponseRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        profile_type, vendor = request.user.get_profile()
        slug = self.kwargs.get("slug") or "0"
        _id = revert_generated_unique_id(None, slug)
        queryset = get_object_or_404(RFQResponse, pk=_id)

        isContract = request.query_params.get("for") is not None
        extras = {}
        if isContract:
            contract = (
                RFQContract.objects.select_related("rfq_response")
                .filter(rfq=queryset.rfq, rfq_response=queryset)
                .first()
            )
            if contract:
                extras.update(
                    {
                        "contract": {
                            "id": contract.pk,
                            "officer": {
                                "id": contract.officer.pk,
                                "name": contract.officer.name,
                            },
                            "terms_and_conditions": contract.terms_and_conditions,
                        }
                    }
                )

        serializer = self.get_serializer(queryset)
        auth_perms = {
            "update": request.user.profile in queryset.rfq.opened_by.all(),
        }

        return Response(
            {"data": serializer.data, "auth_perms": auth_perms, "extras": extras},
            status=status.HTTP_200_OK,
        )
