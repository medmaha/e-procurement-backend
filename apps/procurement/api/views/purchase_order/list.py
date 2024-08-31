from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.procurement.models import PurchaseOrder
from apps.procurement.api.serializers.purchase_order import PurchaseOrderListSerializer


class PurchaseOrderListView(ListAPIView):
    serializer_class = PurchaseOrderListSerializer

    def get_queryset(self):
        return PurchaseOrder.objects.filter()

    def list(self, request, *args, **kwargs):
        profile_type, staff = request.user.get_profile()

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        auth_perms = {
            "create": request.user.has_perm("procurement.add_purchaseorder"),
            "read": request.user.has_perm("procurement.view_purchaseorder"),
            "update": request.user.has_perm("procurement.change_purchaseorder"),
            "delete": request.user.has_perm("procurement.delete_purchaseorder"),
        }

        return Response(
            {"data": serializer.data, "auth_perms": auth_perms},
        )
