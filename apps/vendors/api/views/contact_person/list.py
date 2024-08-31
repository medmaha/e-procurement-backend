import threading
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.vendors.models import ContactPerson
from apps.vendors.api.serializers.contact_person import ContactPersonListSerializer


class ContactPersonListView(ListAPIView):
    serializer_class = ContactPersonListSerializer

    def list(self, request, *args, **kwargs):
        profile_type, profile = request.user.get_profile()
        query = {}

        if profile_type == "Vendor":
            query.update({"vendors": profile})

        many = "vendor" not in query
        queryset = ContactPerson.objects.filter(**query)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
