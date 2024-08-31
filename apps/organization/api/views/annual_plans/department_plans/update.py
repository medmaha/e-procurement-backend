from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.organization.models import Staff, AnnualPlan
from apps.accounts.models import Account
from APP_COMPANY import APP_CONSTANTS


class AnnualProcurementApprovalView(UpdateAPIView):
    def compare_staffs(self, staffs):
        "Compares and returns a staff to approve the annual plan"
        return staffs[0]

    def update(self, request, *args, **kwargs):
        user: Account = request.user
        profile_name, profile = user.get_profile()
        annual_plan_id = request.data.get("id")
        annual_plan = AnnualPlan.objects.filter(id=annual_plan_id).first()
        if not annual_plan:
            return Response(
                {"success": False, "message": "Found no matching annual plan"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not annual_plan.approvable:
            return Response(
                {"message": "Plan is invalid for approval"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group_name = APP_CONSTANTS["GROUPS"]["Annual Procurement Approver"]["name"]
        accounts = Account.objects.filter(
            group__name__iexact=group_name, is_active=True
        )

        if not accounts.exists():
            return Response(
                {"message": "Your organization has no staff to approve the plan"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Plan approval sent to all approvers",
            },
        )
