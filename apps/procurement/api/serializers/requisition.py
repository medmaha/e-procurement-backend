import re
from rest_framework import serializers
from apps.procurement.models import Requisition, RequisitionItem, RequisitionApproval
from apps.organization.models import Staff


class RequisitionApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionApproval
        fields = [
            "unit_approval",
            "department_approval",
            "procurement_approval",
            "finance_approval",
            "stage",
        ]


class RequisitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionItem
        fields = "__all__"


# ==================================== CREATE ================================#
class RequisitionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = ["remarks"]


# ==================================== UPDATE ================================#
class RequisitionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = ["remarks"]


# ==================================== List ================================#
class RequisitionListApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionApproval
        fields = ["id", "status", "editable", "stage"]

    def to_representation(self, instance: RequisitionApproval):
        data = super().to_representation(instance)
        array = (
            ("unit_approval", instance.unit_approval),
            ("department_approval", instance.department_approval),
            ("procurement_approval", instance.procurement_approval),
            ("finance_approval", instance.finance_approval),
        )
        for item in array:
            name, model = item
            data[name] = {}
            if model:
                data[name]["id"] = str(model.pk)
                data[name]["status"] = str(model)
            else:
                data[name]["status"] = "N/A"
                data[name]["id"] = None

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            data["apposable"] = instance.has_approve_perm(request.user)

        data["procurement_method"] = instance.procurement_method
        return data


class RequisitionListOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "name"]

    def to_representation(self, instance: Staff):
        data = super().to_representation(instance)

        data["unit"] = {"id": instance.unit.pk, "name": instance.unit.name}
        data["department"] = {
            "id": instance.unit.department.pk,
            "name": instance.unit.department.name,
        }

        return data


class RequisitionListSerializer(serializers.ModelSerializer):
    officer = RequisitionListOfficerSerializer(read_only=True)
    approval = serializers.SerializerMethodField()
    items = RequisitionItemSerializer(many=True)

    class Meta:
        model = Requisition
        fields = [
            "id",
            "items",
            "remarks",
            "request_type",
            "officer",
            "remarks",
            "approval",
            "created_date",
            "last_modified",
        ]

    def get_approval(self, obj):
        return RequisitionListApprovalSerializer(
            instance=obj.approval_record, context=self.context
        ).data


# ==================================== RETRIEVE ================================#
class RequisitionSelectSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Requisition
        fields = ["unique_id", "id", "name"]

    def get_name(self, obj: Requisition):
        name = f" | ".join([i.description for i in obj.items.all()[:2]])
        return name[:50]


# ==================================== RETRIEVE ================================#
class RequisitionRetrieveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitionApproval
        fields = [
            "id",
            "unique_id",
            "status",
            "editable",
            "stage",
            "procurement_method",
            "created_date",
            "last_modified",
        ]

    def apposable(self, data: RequisitionApproval):
        if "request" not in self.context:
            return False
        _stage = ["Unit", "Department", "Procurement", "Finance"]
        _list = [
            "unit_approval",
            "department_approval",
            "procurement_approval",
            "finance_approval",
        ]
        for item in zip(_stage, _list):
            stage, approval = item
            if data.stage == stage:
                if not getattr(data, approval):
                    return True

        return False

    def to_representation(self, instance: RequisitionApproval):
        data = super().to_representation(instance)
        data["apposable"] = self.apposable(instance)
        array = (
            ("unit_approval", instance.unit_approval),
            ("department_approval", instance.department_approval),
            ("procurement_approval", instance.procurement_approval),
            ("finance_approval", instance.finance_approval),
        )
        for item in array:
            name, model = item
            data[name] = {}
            if model:
                data[name]["id"] = str(model.pk)
                data[name]["status"] = str(model)
                data[name]["remark"] = model.remark
                data[name]["created_date"] = model.created_date
                data[name]["last_modified"] = model.last_modified

                if name == "finance_approval":
                    data[name]["funds_confirmed"] = model.funds_confirmed  # type: ignore

                if name == "procurement_approval":
                    data[name][
                        "part_of_annual_plan"
                    ] = instance.procurement_approval.part_of_annual_plan  # type:ignore
                    if instance.procurement_approval:
                        data[name]["annual_procurement_plan"] = {
                            "id": (
                                instance.procurement_approval.annual_procurement_plan.pk
                                if instance.procurement_approval.annual_procurement_plan
                                else None
                            ),  # type:ignore
                            "description": (
                                instance.procurement_approval.annual_procurement_plan.description
                                if instance.procurement_approval.annual_procurement_plan
                                else None
                            ),  # type:ignore
                        }

            else:
                data[name]["status"] = "N/A"
                data[name]["id"] = None

        return data


class RequisitionRetrieveOfficerSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ["id", "name", "unit", "department"]

    def get_unit(self, obj):
        data = {
            "id": obj.unit.pk if obj.unit else None,
            "name": obj.unit.name if obj.unit else None,
        }
        return data

    def get_department(self, obj):
        data = {
            "id": obj.department.pk if obj.department else None,
            "name": obj.department.name if obj.department else None,
        }
        return data


class RequisitionRetrieveSerializer(serializers.ModelSerializer):
    officer = RequisitionRetrieveOfficerSerializer()
    approval = serializers.SerializerMethodField(read_only=True)
    items = RequisitionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Requisition
        fields = [
            "id",
            "request_type",
            "officer",
            "items",
            "remarks",
            "approval",
            "created_date",
            "last_modified",
        ]

    def unit_approval(self, obj: RequisitionApproval):
        try:
            if not obj.unit_approval:
                raise ValueError("")

            return {
                "id": obj.unit_approval.pk,
                "name": "Unit Approval",
                "approve": obj.unit_approval.approve,
                "officer": {
                    "id": obj.unit_approval.officer.pk,  # type: ignore
                    "name": obj.unit_approval.officer.name,  # type: ignore
                },
                "remark": obj.unit_approval.remark,
                "created_date": obj.unit_approval.created_date,
            }
        except:
            return {
                "id": 0,
                "name": "Unit Approval",
            }

    def department_approval(self, obj: RequisitionApproval):
        try:
            if not obj.department_approval:
                raise ValueError("")

            return {
                "id": obj.department_approval.pk,
                "name": "Department Approval",
                "approve": obj.department_approval.approve,
                "officer": {
                    "id": obj.department_approval.officer.pk,  # type: ignore
                    "name": obj.department_approval.officer.name,  # type: ignore
                },
                "remark": obj.department_approval.remark,
                "created_date": obj.department_approval.created_date,
            }
        except:
            return {
                "id": 0,
                "name": "Department Approval",
            }

    def procurement_approval(self, obj: RequisitionApproval):

        try:
            if not obj.procurement_approval:
                raise ValueError("")

            return {
                "id": obj.procurement_approval.pk,
                "name": "Procurement Approval",
                "approve": obj.procurement_approval.approve,
                "part_of_annual_plan": obj.procurement_approval.part_of_annual_plan,
                "annual_procurement_plan": {
                    "id": str(obj.procurement_approval.annual_procurement_plan.pk),  # type: ignore
                    "title": str(obj.procurement_approval.annual_procurement_plan),
                },
                "officer": {
                    "id": obj.procurement_approval.officer.pk,  # type: ignore
                    "name": obj.procurement_approval.officer.name,  # type: ignore
                },
                "remark": obj.procurement_approval.remark,
                "created_date": obj.procurement_approval.created_date,
            }

        except:
            return {
                "id": 0,
                "name": "Department Approval",
            }

    def finance_approval(self, obj: RequisitionApproval):

        try:
            if not obj.finance_approval:
                raise ValueError("")

            return {
                "id": obj.finance_approval.pk,
                "name": "Finance Approval",
                "approve": obj.finance_approval.approve,
                "funds_confirmed": obj.finance_approval.funds_confirmed,
                "officer": {
                    "id": obj.finance_approval.officer.pk,  # type: ignore
                    "name": obj.finance_approval.officer.name,  # type: ignore
                },
                "remark": obj.finance_approval.remark,
                "created_date": obj.finance_approval.created_date,
            }

        except:
            return {
                "name": "Department Approval",
            }

    def get_approval(self, instance: Requisition):
        try:
            approval: RequisitionApproval = instance.approval_record  # type: ignore
        except:
            return None
        data = {}

        data["id"] = approval.pk
        data["stage"] = approval.stage
        data["status"] = approval.status
        data["editable"] = approval.editable
        data["created_date"] = approval.created_date
        data["procurement_method"] = approval.procurement_method

        data["unit_approval"] = self.unit_approval(approval)
        data["department_approval"] = self.department_approval(approval)
        data["procurement_approval"] = self.procurement_approval(approval)
        data["finance_approval"] = self.finance_approval(approval)

        return data
