from rest_framework import serializers

from apps.organization.models import Unit, Staff, Department
from apps.organization.api.serializers.department import DepartmentRetrieveSerializer


# ============================== Unit Selection ================================== #


class UnitSelectionSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ["id", "name", "department"]

    def get_department(self, obj: Unit):
        return obj.department.name


class UnitHead(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "full_name"]


class UnitListDepartmentView(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class UnitListHeadView(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class UnitListSerializer(serializers.ModelSerializer):
    unit_head = UnitHead()
    staffs = serializers.SerializerMethodField()
    department = UnitListDepartmentView()
    unit_head = UnitListHeadView()

    class Meta:
        model = Unit
        fields = [
            "id",
            "name",
            "description",
            "unit_head",
            "department",
            "staffs",
            "phone",
            "disabled",
            # "created_date",
            # "last_modified",
        ]

    def get_staffs(self, obj):
        staffs = Staff.objects.filter(unit=obj).values("id", "first_name", "last_name")[
            :4
        ]
        return staffs


class UnitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["name", "description", "department", "phone", "unit_head"]


class UnitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["name", "description", "department", "unit_head", "phone"]


class UnitRetrieveSerializer(serializers.ModelSerializer):
    staffs = serializers.SerializerMethodField()
    unit_head = serializers.SerializerMethodField()
    department = DepartmentRetrieveSerializer()

    class Meta:
        model = Unit
        fields = [
            "id",
            "unique_id",
            "name",
            "description",
            "phone",
            "unit_head",
            "staffs",
            "department",
            "created_date",
            "last_modified",
            "enabled_since",
        ]

    def get_unit_head(self, obj):
        head = (
            Staff.objects.filter(leading_unit=obj)
            .values("id", "first_name", "last_name")
            .first()
        )
        return head

    def get_staffs(self, obj):
        staffs = Staff.objects.filter(unit=obj).values(
            "id", "first_name", "last_name", "job_title"
        )[:4]
        return staffs


class UnitRetrieveUpdateSerializer(serializers.ModelSerializer):
    unit_head = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = [
            "name",
            "description",
            "phone",
            "unit_head",
            "department",
        ]

    def get_unit_head(self, obj):
        head = (
            Staff.objects.filter(leading_unit=obj)
            .values("id", "first_name", "last_name")
            .first()
        )
        return head

    def get_department(self, obj: Unit):
        return {"id": obj.department.pk, "name": obj.department.name}
