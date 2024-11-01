import re
from rest_framework import serializers
from apps.procurement.models import Requisition, RequisitionItem, RequisitionApproval
from apps.organization.models import Staff
from apps.procurement.models.pr_approval_action import ApprovalAction


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
    current_approver = serializers.SerializerMethodField()
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
            "current_approval_step",
            "approval_status",
            "created_date",
            "last_modified",
            "current_approver",
        ]

    def get_current_approver(self, instance: Requisition):
        # return RequisitionListApprovalSerializer(
        #     instance=obj.approval_record, context=self.context
        # ).data
        if not instance.current_approval_step:
            return False

        workflow_step = instance.current_approval_step

        if workflow_step and workflow_step.step.approver is None:
            return False

        return {
            "id": workflow_step.step.approver.pk,
            "name": workflow_step.step.approver.name,
        }


# ==================================== RETRIEVE ================================#
class RequisitionSelectSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Requisition
        fields = ["id", "name", "created_date"]

    def get_name(self, obj: Requisition):
        name = f" | ".join([i.description for i in obj.items.all()[:2]])
        return name[:50]


# ==================================== RETRIEVE ================================#
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
    approvals = serializers.SerializerMethodField(read_only=True)
    current_approval_step = serializers.SerializerMethodField(read_only=True)
    items = RequisitionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Requisition
        fields = [
            "id",
            "request_type",
            "officer",
            "items",
            "remarks",
            "approvals",
            "approval_status",
            "current_approval_step",
            "created_date",
            "last_modified",
        ]

    def get_current_approval_step(self, instance: Requisition):

        if instance.current_approval_step:
            workflow_step = instance.current_approval_step
            return {
                "id": workflow_step.pk,
                "order": workflow_step.order,
                "step": {
                    "id": workflow_step.step.pk,
                    "name": workflow_step.step.name,
                    "order": workflow_step.step.order,
                    "approver": (
                        {
                            "id": workflow_step.step.approver.pk,
                            "name": workflow_step.step.approver.name,
                            "avatar": workflow_step.step.approver.user_account.avatar,
                            "job_title": workflow_step.step.approver.job_title,
                            "unit": {
                                "id": workflow_step.step.approver.unit.pk,
                                "name": workflow_step.step.approver.unit.name,
                                "department": {
                                    "id": workflow_step.step.approver.department.pk,
                                    "name": workflow_step.step.approver.department.name,
                                },
                            },
                        }
                        if workflow_step.step.approver
                        else None
                    ),
                },
                "workflow": {
                    "id": workflow_step.workflow.pk,
                    "name": workflow_step.workflow.name,
                    "steps": workflow_step.workflow.steps.count(),
                },
                "id": workflow_step.pk,
            }

        return None

    def get_approvals(self, instance: Requisition):
        approvals = ApprovalAction.objects.filter(requisition=instance)

        data = [
            {
                "id": approval.pk,
                "action": approval.action,
                "comments": approval.comments,
                "created_date": approval.created_date,
                "last_modified": approval.last_modified,
                "workflow_step": (
                    {
                        "id": approval.workflow_step.pk,
                        "order": approval.workflow_step.order,
                        "step": {
                            "id": approval.workflow_step.step.pk,
                            "order": approval.workflow_step.step.order,
                            "name": approval.workflow_step.step.order,
                        },
                        "workflow": {
                            "id": approval.workflow_step.workflow.pk,
                            "name": approval.workflow_step.workflow.name,
                            "steps": approval.workflow_step.workflow.steps.count(),
                        },
                        "id": approval.workflow_step.pk,
                    }
                    if approval.workflow_step
                    else None
                ),
                "approver": {
                    "id": approval.approver.pk,
                    "name": approval.approver.name,
                    "avatar": approval.approver.user_account.avatar,
                    "job_title": approval.approver.job_title,
                    "unit": {
                        "id": approval.approver.unit.pk,
                        "name": approval.approver.unit.name,
                        "department": (
                            {
                                "id": approval.approver.department.pk,
                                "name": approval.approver.department.name,
                            }
                            if approval.approver.department
                            else None
                        ),
                    },
                },
            }
            for approval in approvals
        ]

        return data

    def to_representation(self, instance: Requisition):
        data = super().to_representation(instance)

        data["officer_department"] = (
            {
                "id": instance.officer_department.pk,
                "name": instance.officer_department.name,
            }
            if instance.officer_department
            else None
        )

        return data
