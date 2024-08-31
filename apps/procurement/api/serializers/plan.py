from rest_framework import serializers

from apps.organization.models import DepartmentProcurementPlan, PlanItem
from apps.procurement.models import Requisition


class PlanItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItem
        fields = "__all__"


class ProcurementPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentProcurementPlan
        fields = "__all__"
