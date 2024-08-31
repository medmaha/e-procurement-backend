from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView

from apps.procurement.models import RFQ
from apps.organization.models.staff import Staff
from apps.accounts.models.account import Account


class OpenedStaffsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "job_title", "employee_id", "name"]

    def to_representation(self, instance: Staff):
        data = super().to_representation(instance)
        data["department"] = (
            {"id": instance.department.pk, "name": instance.department.name}
            if instance.department
            else None
        )
        return data


class RfqOpenedByView(RetrieveAPIView):
    serializer_class = OpenedStaffsSerializer

    def get_queryset(self, rfq_id):
        if rfq_id:
            rfq = get_object_or_404(RFQ, pk=rfq_id)
            queryset = rfq.opened_by.filter()
        else:
            accounts = Account.objects.filter(
                groups__in=Group.objects.filter(name__iexact="RFQ Response Opener")
            )
            queryset = Staff.objects.filter(user_account__in=accounts)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        rfq_id = kwargs.get("rfq_id")
        queryset = self.get_queryset(rfq_id)
        serializer = self.get_serializer(instance=queryset, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
