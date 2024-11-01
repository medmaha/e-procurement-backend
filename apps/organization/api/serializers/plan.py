from rest_framework import serializers

from apps.organization.models import (
    DepartmentProcurementPlan,
    PlanItem,
    AnnualPlan,
    Threshold,
)


class PlanItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItem
        fields = [
            "id",
            "description",
            "quantity",
            "budget",
            "measurement_unit",
            # "procurement_method",
            "quarter_1_budget",
            "quarter_2_budget",
            "quarter_3_budget",
            "quarter_4_budget",
        ]

    # def _validate_budget(self, value: int):
    #     matching_threshold = Threshold.get_matching_threshold(value)
    #     if not matching_threshold:
    #         raise serializers.ValidationError("Budget not in threshold")

    #     if self.instance:
    #         self.instance.procurement_method = matching_threshold.procurement_method
    #     return value


class DepartmentProcurementPlanListSerializer(serializers.ModelSerializer):
    items = PlanItemListSerializer(many=True)

    class Meta:
        model = DepartmentProcurementPlan
        fields = ["id", "description", "items", "created_date"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["department"] = {
            "id": instance.department.id,
            "name": instance.department.name,
            "description": instance.department.description[:50],
        }
        return data


class DepartmentProcurementPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentProcurementPlan
        fields = [
            "description",
        ]

    # def validate(self, attr):
    #     if not Threshold.objects.filter().exists():
    #         raise serializers.ValidationError(
    #             "Annual Procurement Can't be applied. GPPA Thresholds not available"
    #         )
    #     return attr


class AnnualPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnualPlan
        fields = [
            "id",
            "title",
            "description",
            "year_start",
        ]


class AnnualPlanRetrieveSerializer(serializers.ModelSerializer):
    department_plans = DepartmentProcurementPlanListSerializer(many=True)

    class Meta:
        model = AnnualPlan
        fields = [
            "id",
            "title",
            "description",
            "department_plans",
            "org_approved",
            "gppa_approved",
            "is_operational",
            "created_date",
        ]

    def to_representation(self, instance: AnnualPlan):
        data = super().to_representation(instance)
        request = self.context.get("request")
        data["officer"] = (
            (
                {
                    "id": instance.officer.pk,
                    "name": instance.officer.name,
                    "employee_id": instance.officer.employee_id,
                    "unit": {
                        "id": instance.officer.unit.pk,
                        "name": instance.officer.unit.name,
                        "department": {
                            **(
                                {
                                    "id": instance.officer.department.pk,
                                    "name": instance.officer.department.name,
                                }
                                if instance.officer.department
                                else {}
                            )
                        },
                    },
                }
            )
            if instance.officer
            else None
        )
        if request and instance.officer == request.user.profile:
            data["request_for_approval_both"] = not (
                instance.org_approved or instance.gppa_approved
            )
            if not data["request_for_approval_both"]:
                data["request_for_approval_org"] = not instance.org_approved

                if not data.get("request_for_approval_org"):
                    data["request_for_approval_gppa"] = not instance.gppa_approved

        return data


class DepartmentProcurementPlanSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentProcurementPlan
        fields = ["id", "title"]


class PlanItemSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItem
        fields = ["id", "description"]
