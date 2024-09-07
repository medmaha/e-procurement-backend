from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.core.utilities.errors import get_serializer_error_message

from apps.app.serializers.company import (
    CompanyCreateSerializer,
    CompanyRetrieveSerializer,
)


class CompanyCreateAPIView(CreateAPIView):

    serializer_class = CompanyCreateSerializer

    def create(self, request, *args, **kwargs):

        data = request.data

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            company = serializer.save()
            result_serializer = CompanyRetrieveSerializer(instance=company)
            return Response(result_serializer.data, status=201)

        error_message = get_serializer_error_message(serializer)
        return Response({"error": error_message}, status=400)
