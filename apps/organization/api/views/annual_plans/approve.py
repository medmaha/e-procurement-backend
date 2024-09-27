from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import AnnualPlan
from apps.accounts.models import Account
from APP_COMPANY import APP_CONSTANTS
from apps.organization.models.procurement_plan import (
    AnnualPlanApproval,
    AnnualPlanApprovalGPPA,
)


class AnnualPlanApprovalView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()

        annual_plan_id = request.data.get("id")
        annual_plan = get_object_or_404(AnnualPlan, id=annual_plan_id)

        if not annual_plan.approvable:
            return Response(
                {"message": "Plan is invalid for approval"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # TODO: implement a better solution for this
        group_name = APP_CONSTANTS["GROUPS"]["Annual Procurement Approver"]["name"]
        accounts = Account.objects.filter(
            groups__name__iexact=group_name, is_active=True
        )

        if not accounts.exists():
            return Response(
                {
                    "message": "Your organization has no staff authorized to approve the plan"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if profile_name == "Staff":
            approval = AnnualPlanApproval.objects.filter(annual_plan=annual_plan).last()
            if approval:
                return Response(
                    {
                        "success": False,
                        "message": "Plan has already been approved by %s"
                        % str(approval.officer or "Staff"),
                    }
                )
            approval = AnnualPlanApproval(
                annual_plan=annual_plan,
                # officer=profile
            )

        return Response(
            {
                "success": True,
                "message": "Plan approval sent to all approvers",
            },
        )
