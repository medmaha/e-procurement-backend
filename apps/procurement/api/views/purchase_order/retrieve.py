from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.procurement.models import PurchaseOrder
from apps.procurement.api.serializers.purchase_order import (
    PurchaseOrderRetrieveSerializer,
)


class PurchaseOrderRetrieveView(RetrieveAPIView):
    serializer_class = PurchaseOrderRetrieveSerializer

    def get_queryset(self):
        return PurchaseOrder.objects.filter(pk=self.kwargs.get("id")).first()

    def retrieve(self, request, *args, **kwargs):
        profile_type, staff = request.user.get_profile()

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, context={"request": request})

        auth_perms = {
            "create": request.user.has_perm("procurement.add_purchaseorder"),
            "read": request.user.has_perm("procurement.view_purchaseorder"),
            "update": request.user.has_perm("procurement.change_purchaseorder"),
            "delete": request.user.has_perm("procurement.delete_purchaseorder"),
        }

        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
        )
