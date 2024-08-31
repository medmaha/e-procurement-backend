from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.procurement.models.rfq import RFQ
from apps.procurement.models.rfq_approval import (
    RFQApproval,
    RFQApprovalGPPA,
    ApprovalChoices,
)
from apps.core.utilities.text_choices import RFQLevelChoices


class RFQApprovalView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        profile_type, profile = user.get_profile()

        data = request.data.copy()
        rfq = get_object_or_404(RFQ, pk=data.pop("rfq_id") if "rfq_id" in data else 0)

        rfq_approval, created = RFQApproval.objects.get_or_create(rfq=rfq)
        is_approved = data.get("approve").lower() == "yes"
        approve_text = (
            ApprovalChoices.ACCEPTED.value
            if is_approved
            else ApprovalChoices.REJECTED.value
        )

        if profile_type == "GPPA":
            gppa_approval, _ = RFQApprovalGPPA.objects.get_or_create(
                officer=user, rfq_id=rfq.pk
            )
            if gppa_approval.approve == approve_text:
                return Response(
                    {"message": "This RFQ been approved by a %s user" % profile_type},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            gppa_approval.approve = approve_text
            gppa_approval.remarks = data.get("remark", "")
            gppa_approval.save()
            rfq_approval.gppa_approval = gppa_approval
            rfq_approval.approve = approve_text
            rfq_approval.save()
        elif profile_type == "Staff":
            if not created and not rfq_approval.gppa_approval:
                return Response(
                    {
                        "message": (
                            'This RFQ was approved by "%s" and now requires GPPA Approval'
                            % rfq_approval.officer.name
                            if rfq_approval.officer
                            else "a Staff"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if rfq_approval.officer:
                return Response(
                    {
                        "message": 'This RFQ was approved by "%s".'
                        % rfq_approval.officer.name
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            rfq_approval.remarks = data.get("remark", "")
            rfq_approval.approve = approve_text
            rfq_approval.officer = profile
            rfq_approval.save()

        return Response(
            {
                "message": (
                    "RFQ %s successfully" % "Approved" if is_approved else "Declined"
                )
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, *args, **kwargs):
        user = request.user
        profile_type, profile = user.get_profile()

        data = request.data.copy()
        rfq = get_object_or_404(RFQ, pk=data.pop("rfq_id") if "rfq_id" in data else 0)

        if not rfq.level in [
            RFQLevelChoices.APPROVAL_LEVEL.value,
            RFQLevelChoices.PUBLISH_LEVEL.value,
        ]:
            return Response(
                {
                    "message": "This RFQ cannot be published or has already past the publish level"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rfq_approval = get_object_or_404(RFQApproval, rfq=rfq)
        publish = "publish" in request.data
        if not publish:
            return Response(
                {"message": "Invalid form-data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if rfq_approval.rfq.requires_gppa_approval and not rfq_approval.gppa_approval:
            return Response(
                {"message": "This RFQ requires an Approval from GPPA"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rfq.published = True
        rfq.save()
        return Response(
            {"message": "RFQ Approved and Published successfully"},
            status=status.HTTP_201_CREATED,
        )
