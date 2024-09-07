from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from apps.app.models.company import Company
from apps.app.serializers.company import CompanyRetrieveSerializer


class CompanyRetrieveAPIView(RetrieveAPIView):

    serializer_class = CompanyRetrieveSerializer

    def get_queryset(self, slug: str):
        try:
            queryset = Company.objects.get(slug=slug)
        except:
            return None
        return queryset

    def retrieve(self, request, slug: str, *args, **kwargs):
        queryset = self.get_queryset(slug)
        if queryset is None:
            return Response({"error": "Company not found"}, status=404)

        serializer = self.get_serializer(queryset)

        return Response(serializer.data)
