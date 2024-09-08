from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.organization.models.staff import Staff
from apps.organization.api.serializers.staff import StaffRetrieveSerializer


class StaffGetAPIView(RetrieveAPIView):

    serializer_class = StaffRetrieveSerializer

    def get_queryset(self, staff_id: str):
        try:
            queryset = Staff.objects.get(id=staff_id)
        except:
            return None
        return queryset

    def retrieve(self, request, staff_id: str, *args, **kwargs):
        queryset = self.get_queryset(staff_id)
        if queryset is None:
            return Response({"error": "Staff not found"}, status=404)

        serializer = self.get_serializer(queryset)

        return Response(serializer.data)
