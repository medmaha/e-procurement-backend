from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


from apps.app.models.company import Company
from apps.app.serializers.company import CompanyQuerySerializer


class CompanyQueryAPIView(ListAPIView):

    serializer_class = CompanyQuerySerializer

    def get_queryset(self, query: str):
        if not query:
            return []

        queryset = Company.objects.filter(
            Q(name__icontains=query)
            | Q(industry__icontains=query)
            | Q(description__icontains=query)
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request.query_params.get("q"))
        serializer = self.get_serializer(queryset, many=True)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
