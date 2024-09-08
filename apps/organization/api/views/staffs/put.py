from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.organization.models import Staff
from apps.organization.api.serializers.staff import (
    StaffUpdateSerializer,
    StaffRetrieveSerializer,
)


class StaffUpdateAPIView(UpdateAPIView):

    serializer_class = StaffUpdateSerializer

    def get_queryset(self, staff_id: str):
        try:
            queryset = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return None
        return queryset

    def update(self, request, staff_id: str, *args, **kwargs):
        queryset = self.get_queryset(staff_id)
        if queryset is None:
            return Response({"error": "Staff not found"}, status=404)

        data = request.data

        serializer = self.get_serializer(instance=queryset, data=data)

        if serializer.is_valid():
            staff = serializer.save()
            result_serializer = StaffRetrieveSerializer(instance=staff)
            return Response(result_serializer.data, status=200)

        error_message = str(serializer.errors)
        return Response({"error": error_message}, status=400)
