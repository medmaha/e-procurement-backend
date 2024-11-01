from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.procurement.models.rfq import RFQ
from apps.procurement.models.rfq_approval import (
    RFQApproval,
    ApprovalChoices,
)


class RFQApprovalView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile

        # TODO: check for permission

        data = request.data.copy()

        rfq = RFQ.objects.only("id").get(pk=data.pop("rfq_id", 0))
        rfq_approval = RFQApproval.objects.only("id").filter(rfq=rfq)

        if rfq_approval.exists():
            rfq_approval = rfq_approval.first()
            return Response(
                {
                    "message": (
                        'This RFQ was approved by "%s" and now requires GPPA Approval'
                        % rfq_approval.officer.name
                        if rfq_approval and rfq_approval.officer
                        else "a Staff"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_approved = data.get("approve", False)
        approve_text = (
            ApprovalChoices.APPROVED.value
            if is_approved
            else ApprovalChoices.REJECTED.value
        )

        rfq_approval = RFQApproval()
        rfq_approval.rfq = rfq
        rfq_approval.remarks = data.get("remark", "")
        rfq_approval.approve = approve_text
        rfq_approval.officer = profile
        rfq_approval.full_clean()

        # This dispatches a post_save signal for it's Instance
        rfq_approval.save()

        return Response(
            {
                "message": (
                    "RFQ %s successfully" % "Approved" if is_approved else "Rejected"
                )
            },
            status=status.HTTP_201_CREATED,
        )
