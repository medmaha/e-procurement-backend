from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.organization.models.company import Company
from apps.organization.api.serializers.company import CompanyQuerySerializer


class CompanyListAPIView(ListAPIView):

    serializer_class = CompanyQuerySerializer

    def get_queryset(self):
        queryset = Company.objects.filter()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
