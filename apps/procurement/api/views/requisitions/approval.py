from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.accounts.models import Account
from apps.procurement.models import Requisition

from apps.core.utilities.text_choices import ApprovalChoices
from apps.procurement.models.pr_approval_action import ApprovalAction


class RequisitionApprovalView(APIView):

    def put(self, request, slug, *args, **kwargs):

        try:
            with transaction.atomic():

                instance = get_object_or_404(Requisition, pk=slug)

                workflow_step = instance.current_approval_step

                if workflow_step is None:
                    return Response(
                        {"detail": "Forbidden! Workflow step not found"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                profile = request.user.profile

                comments = request.data.get("comments", None)
                print(request.data)
                approved = request.data.get("action", "rejected") in [
                    True,
                    "true",
                    "approved",
                ]

                if approved:
                    action = ApprovalChoices.APPROVED
                else:
                    error_msg = None
                    if not comments:
                        error_msg = f"Comments is required when rejecting a requisition"
                    if len(comments) < 10:
                        error_msg = f"Comments must be at least 10 characters long"
                    if len(comments) > 500:
                        error_msg = f"Comments must be less than 500 characters long"
                    if error_msg:
                        return Response(
                            {"message": error_msg}, status=status.HTTP_400_BAD_REQUEST
                        )
                    action = ApprovalChoices.REJECTED

                approval = ApprovalAction(
                    action=action,
                    approver=profile,
                    requisition=instance,
                    comments=request.data.get("comments", ""),
                    workflow_step=instance.current_approval_step,
                )
                approval.full_clean()
                approval.save()
                approval.move_to_next_step()

                return Response(
                    {"message": "Action taken successfully"}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
