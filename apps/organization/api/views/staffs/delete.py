from django.utils import timezone

from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView

from apps.organization.models import Staff


class StaffDisableAPIView(DestroyAPIView):

    def get_queryset(self, staff_id: str):
        try:
            queryset = Staff.objects.get(pk=staff_id)
        except:
            return None
        return queryset

    def destroy(self, request, staff_id: str, *args, **kwargs):

        queryset = self.get_queryset(staff_id)

        if queryset is None:
            return Response({"error": "Staff not found"}, status=404)

        queryset.is_deleted = True
        queryset.date_deleted = timezone.now()
        queryset.save()

        return Response({"message": "Staff deleted successfully"}, status=204)
