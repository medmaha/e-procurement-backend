from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView


from apps.accounts.models import AuthGroup


class GroupDisableAPIView(DestroyAPIView):
    """
    Delete a group
    """

    def get_queryset(self, group_id, author_id):

        try:
            return AuthGroup.objects.get(
                id=group_id, authored_by=author_id, editable=True, is_deleted=False
            )
        except AuthGroup.DoesNotExist:
            return None

    def destroy(self, request, group_id, *args, **kwargs):
        """
        Delete a group, This does not delete the group permissions

        """

        profile_name, profile = request.user.get_profile()

        if profile_name.lower() != "staff":
            return Response(
                {"error": "Permission denied!"}, status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_queryset(group_id, str(profile.pk))

        if not instance:
            return Response(
                {"error": "Permission Error or Group not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.is_deleted = True
        instance.date_deleted = timezone.now()
        instance.save()

        # TODO: delete group permissions

        return Response(
            {"message": "Group deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
