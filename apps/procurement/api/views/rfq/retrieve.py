from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.procurement.api.serializers.quotations import RFQItemsSerializer
from apps.procurement.models import RFQ, RFQApproval
from apps.procurement.api.serializers.rfq import (
    RFQListSerializer,
)
from apps.core.utilities.generators import revert_generated_unique_id


class RfqRetrieveView(RetrieveAPIView):
    serializer_class = RFQListSerializer

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            _id = revert_generated_unique_id("RFQ", slug or "0")

            instance = (
                RFQ.objects.prefetch_related("items", "suppliers", "opened_by")
                .select_related("requisition", "officer")
                .get(pk=_id)
            )

            officer = instance.officer  # type: ignore

            if request.query_params.get("only") == "items":
                data = {
                    "officer": (
                        {"id": officer.pk, "name": officer.name} if officer else None
                    ),
                    "requisition": {"id": instance.requisition.pk},  # type: ignore
                    "items": RFQItemsSerializer(instance.items, many=True).data,
                }
            else:
                data = self.get_serializer(instance, context={"request": request}).data

            auth_perms = {
                "read": request.user.has_perm("procurement.view_rfq"),
                "update": request.user.has_perm("procurement.change_rfq"),
                "create": request.user.has_perm("procurement.create_rfq"),
                "approve": request.user.has_perm(
                    f"{RFQApproval._meta.app_label}._add{RFQApproval._meta.model_name}"
                ),
            }

            data = {"data": data, "auth_perms": auth_perms}

            return Response(data, status=status.HTTP_200_OK)

        except RFQ.DoesNotExist:
            return Response(
                {"error": "RFQ not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
