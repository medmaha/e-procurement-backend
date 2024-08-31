from django.db.models import Subquery
from rest_framework import serializers

from apps.organization.models import Staff, Unit, Department
from apps.accounts.models import AuthGroup


class StaffSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "name", "employee_id"]


class Validators:
    def validate_email(self, value):
        "Validates the staff email"
        if not value:
            raise serializers.ValidationError("The staff is required")

        def check_email():
            if Staff.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "This email was already registered to the system"
                )

        instance: Staff = self.instance  # type: ignore
        if instance:
            if instance.email != value:
                check_email()
        else:
            check_email()

        return value

    def validate_unit(self, value):
        if not value:
            raise serializers.ValidationError("The staff unit cannot be empty")
        if hasattr(value, "pk"):
            return value
        if not Unit.objects.filter(pk=value).first():
            raise serializers.ValidationError("The staff unit does not exist")
        return value

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("The staff phone number cannot be empty")

        def check_phone():
            if Staff.objects.filter(phone=value).exists():
                raise serializers.ValidationError("This phone was already registered")

        instance: Staff = self.instance  # type: ignore
        if instance:
            if instance.phone != value:
                check_phone()
        else:
            check_phone()
        return value


# ============================ Staff Crwate ========================= #
class StaffCreateSerializer(serializers.ModelSerializer, Validators):
    class Meta:
        model = Staff
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "job_title",
            "gender",
            "unit",
            "biography",
        ]


# ============================ Staff Update ========================= #
class StaffUpdateSerializer(serializers.ModelSerializer, Validators):
    class Meta:
        model = Staff
        fields = [
            "email",
            "phone",
            "name",
            "email",
            "phone",
            "gender",
            "biography",
        ]


class AdminStaffUpdateSerializer(serializers.ModelSerializer, Validators):
    class Meta:
        model = Staff
        fields = [
            "email",
            "phone",
            "job_title",
            "name",
            "email",
            "phone",
            "unit",
            "gender",
            "biography",
            "disabled",
        ]


# ============================ Staff List ========================= #
class StaffListSerializer(serializers.ModelSerializer):
    def get_changeable(self, instance):
        request = self.context.get("request")
        if not request or instance.disabled:
            return False
        if request.user.profile == instance:
            return True

    def to_representation(self, instance: Staff):
        data = super().to_representation(instance)
        data["unit"] = {
            "id": instance.unit.pk,
            "name": instance.unit.name,
            "department": {
                **(
                    {"id": instance.department.pk, "name": instance.department.name}
                    if instance.department
                    else {}
                )
            },
        }
        data["changeable"] = self.get_changeable(instance)
        return data

    class Meta:
        model = Staff
        fields = [
            "id",
            "name",
            "employee_id",
            "job_title",
            "disabled",
            "biography",
        ]


class StaffRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            "id",
            "employee_id",
            "job_title",
            "user_id",
            "name",
            "email",
            "phone",
            "gender",
            "biography",
            "disabled",
            "created_date",
            "last_modified",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # remove the private fields if request.user is not the staffs
        request = self.context.get("request")
        if request:
            has_perm = request.user.has_perm("organization.add_staff")
            data["is_self"] = instance == request.user.profile
            data["is_admin"] = has_perm
        data["groups"] = self.get_groups(instance)
        # data["created_date"] = instance.created_date
        data["unit"] = {
            "id": instance.unit.pk,
            "name": instance.unit.name,
            "department": {
                **(
                    {"id": instance.department.pk, "name": instance.department.name}
                    if instance.department
                    else {}
                )
            },
        }
        return data

    def get_groups(self, obj):
        groups = obj.user_account.groups.filter()
        sub_query = Subquery(groups.values("pk"))
        auth_groups = AuthGroup.objects.filter(group_id__in=sub_query).order_by(
            "-created_date"
        )

        serializer = auth_groups.values(
            "id", "name", "authored_by", "description", "created_date"
        )
        array = []
        for index, auth_group in enumerate(auth_groups):
            data = dict(serializer[index])
            group = auth_group.group
            data.update({"permissions": group.permissions.count() if group else None})
            array.append(data)

        return array


# FIELDS TO DISPLAY ON STAFF UPDATE FORM API
# ============================ Staff Update Retrieve ========================= #
class StaffUpdateRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            "job_title",
            "first_name",
            "last_name",
            "name",
            "email",
            "phone",
            "gender",
            "biography",
        ]

    def to_representation(self, instance: Staff):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            has_perm = request.user.has_perm("organization.add_staff")
            data["is_self"] = instance == request.user.profile
            data["is_admin"] = has_perm

        data["unit"] = {
            "id": instance.unit.pk,
            "name": instance.unit.name,
        }
        data["groups"] = instance.user_account.groups.filter().values("id", "name")
        return data
