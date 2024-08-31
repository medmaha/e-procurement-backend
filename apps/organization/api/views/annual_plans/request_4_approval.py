from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import AnnualPlan
from apps.accounts.models import Account


class AnnualPlanRequestForApprovalView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        if not AnnualPlan.has_approvers():
            return Response(
                {"message": "There are no approvers for annual plans"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        annual_plan = get_object_or_404(
            AnnualPlan, id=request.data.get("annual_plan_id")
        )

        request_type = request.data.get("request_type")

        if request_type == "ORG":
            if annual_plan.org_approved:
                return Response(
                    {
                        "message": "Plan has already been approved by the organization",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            annual_plan.send_approval_emails(level="ORG")
            return Response(
                {
                    "message": "Plan approval sent to the organization",
                }
            )

        if request_type == "GPPA":
            if annual_plan.gppa_approved:
                return Response(
                    {
                        "message": "Plan has already been approved by GPPA",
                    }
                )
            annual_plan.send_approval_emails(level="GPPA")
            return Response(
                {
                    "message": "Plan approval sent to the organization",
                }
            )

        if request_type == "BOTH":
            if annual_plan.org_approved and annual_plan.gppa_approved:
                return Response(
                    {
                        "message": "Plan has already been approved by both GPPA and the organization",
                    }
                )
            annual_plan.send_approval_emails(level="GPPA")
            return Response(
                {
                    "message": "Plan approval sent to the organization",
                }
            )

        return Response(
            {
                "message": "Invalid approval request type",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
