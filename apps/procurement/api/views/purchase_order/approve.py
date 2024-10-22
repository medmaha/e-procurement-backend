from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.procurement.models.purchase_order import PurchaseOrder, PurchaseOrderApproval
from apps.core.utilities.text_choices import ApprovalChoices


class PurchaseOrderApproveView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        profile_type, staff = request.user.get_profile()

        if profile_type != "Staff" or not request.user.has_perm(
            "procurement.add_purchaseorderapproval"
        ):
            return Response(
                {"message": "You don't have permission to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        purchase_order = get_object_or_404(
            PurchaseOrder, pk=request.data.get("order_id")
        )
        order_approval = PurchaseOrderApproval.objects.filter(parent=purchase_order)
        if order_approval.exists():
            return Response(
                {
                    "message": "You cannot approve this quotation because it has already been approved."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        PurchaseOrderApproval.objects.create(
            parent=purchase_order,
            officer=staff,
            approve=ApprovalChoices.APPROVED.value,
            remarks=request.data.get("remarks", ""),
        )

        if purchase_order.auto_publish:
            purchase_order.published = True
            purchase_order.save()

        return Response(
            {"message": "Purchase order approved successfully"},
            status=status.HTTP_200_OK,
        )
