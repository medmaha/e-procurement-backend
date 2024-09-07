from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from apps.app.models.company import Company
from apps.app.serializers.company import (
    CompanyUpdateSerializer,
    CompanyRetrieveSerializer,
)


class CompanyUpdateAPIView(UpdateAPIView):

    serializer_class = CompanyUpdateSerializer

    def get_queryset(self, slug: str):
        try:
            queryset = Company.objects.get(slug=slug)
        except:
            return None
        return queryset

    def update(self, request, slug: str, *args, **kwargs):
        queryset = self.get_queryset(slug)
        if queryset is None:
            return Response({"error": "Company not found"}, status=404)

        data = request.data

        serializer = self.get_serializer(instance=queryset, data=data)

        if serializer.is_valid():
            company = serializer.save()
            result_serializer = CompanyRetrieveSerializer(instance=company)
            return Response(result_serializer.data, status=200)

        error_message = str(serializer.errors)
        return Response({"error": error_message}, status=400)
