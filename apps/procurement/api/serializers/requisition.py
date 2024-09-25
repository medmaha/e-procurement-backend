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

        data["apposable"] = self.apposable(instance)
        return data

    def apposable(self, data: RequisitionApproval):
        stage = (data.stage + "_approval").lower()
        if hasattr(data, stage):
            if not getattr(data, stage):
                request = self.context.get("request")
                if not request or not request.user:
                    return None
                return request.user.has_perm(
                    "procurement.add_%srequisitionapproval" % data.stage.lower()
                ) or request.user.has_perm(
                    "procurement.change_%srequisitionapproval" % data.stage.lower()
                )
        return False


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
    changeable = serializers.SerializerMethodField()
    items = RequisitionItemSerializer(many=True)

    class Meta:
        model = Requisition
        fields = [
            "id",
            "items",
            "remarks",
            "request_type",
            "changeable",
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

    def get_changeable(self, obj):
        if "request" not in self.context:
            return False
        # if obj.officer == self.context["request"].user.profile:  # type: ignore
        #     return obj.approval_record.stage in [None, "Unit"]
        return False


# ==================================== RETRIEVE ================================#
class RequisitionSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = ["unique_id", "id"]


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
            "unique_id",
            "created_date",
            "last_modified",
        ]

    def get_approval(self, obj):
        try:
            approval = obj.approval_record
        except:
            return None
        serializer = RequisitionRetrieveApprovalSerializer(instance=approval)
        return serializer.data
