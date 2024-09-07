from django.utils import timezone

from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView

from apps.app.models.company import Company
from apps.app.serializers.company import (
    CompanyCreateSerializer,
)


class CompanyDeleteAPIView(DestroyAPIView):

    serializer_class = CompanyCreateSerializer

    def get_queryset(self, slug: str):
        try:
            queryset = Company.objects.get(slug=slug)
        except:
            return None
        return queryset

    def destroy(self, request, slug: str, *args, **kwargs):

        queryset = self.get_queryset(slug)

        if queryset is None:
            return Response({"error": "Company not found"}, status=404)

        queryset.is_deleted = True
        queryset.deleted_at = timezone.now()
        queryset.save()

        return Response({"message": "Company deleted successfully"}, status=204)
