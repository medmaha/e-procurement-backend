from rest_framework import serializers

from apps.organization.models import Department, Unit
from apps.organization.models.staff import Staff


class DepartmentUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name"]

    def to_representation(self, instance: Unit):
        data = super().to_representation(instance)
        if instance.unit_head:
            data["unit_head"] = {
                "id": instance.unit_head.id,
                "name": instance.unit_head.name,
            }
        return data


class DepartmentStaffsSerializer(serializers.ModelSerializer):
    unit = DepartmentUnitsSerializer()

    class Meta:
        model = Staff
        fields = ["id", "name", "unit", "job_title"]


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "email",
            "name",
            "description",
            "phone",
            "disabled",
            "created_date",
        ]

    def to_representation(self, instance: Department):
        data = super().to_representation(instance)
        if instance.department_head:
            data["department_head"] = {
                "id": instance.department_head.pk,
                "name": instance.department_head.name,
            }
        else:
            data["department_head"] = None

        data["units"] = DepartmentUnitsSerializer(
            instance=Unit.objects.filter(department=instance), many=True
        ).data
        return data


class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name", "description", "phone", "email", "department_head_id"]


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name", "description", "phone", "email", "department_head_id"]


class DepartmentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "description",
            "phone",
            "email",
            "department_head",
            "created_date",
            "last_modified",
            "enabled_since",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        units = Unit.objects.filter(department=instance)
        data["units"] = DepartmentUnitsSerializer(instance=units, many=True).data
        data["staffs"] = DepartmentStaffsSerializer(
            instance=Staff.objects.filter(unit__department=instance),
            many=True,
        ).data
        return data
