from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


from apps.organization.models.staff import Staff
from apps.organization.api.serializers.staff import StaffListSerializer


class StaffQueryAPIView(ListAPIView):

    serializer_class = StaffListSerializer

    def get_queryset(self, query: str):
        if not query:
            return []

        queryset = Staff.objects.filter(
            Q(user_account__first_name__icontains=query)
            | Q(user_account__last_name__icontains=query),
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
