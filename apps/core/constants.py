import typing
import apps.procurement.models as proc
import apps.organization.models as org

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class DefaultGroups:
    """
    This class contains the default permission groups used in the system.
    The groups are defined as dictionaries with the following structure:

    {
        "name": str,
        "perms": list[str]
    }

    The "name" key is the name of the group, and the "perms" key is a list of
    permissions that the group should have. The permissions are specified in the
    format "app_label.model_name.permission_name". For example,
    "procurement.requisition.add_requisition" is the permission to add a new
    requisition in the procurement app.
    """

    STAFF_MEMBER: dict[str, typing.Any] = {
        "name": "Staff Members",
        "perms": [
            f"{proc.Requisition._meta.app_label}.add_{proc.Requisition._meta.model_name}",
            f"{proc.Requisition._meta.app_label}.change_{proc.Requisition._meta.model_name}",
            f"{org.Staff._meta.app_label}.view_{org.Staff._meta.model_name}",
        ],
    }

    SUPER_ADMIN: dict[str, typing.Any] = {
        "name": "Super Admin",
        "perms": [
            # Staffs - Create & Update
            f"{org.Staff._meta.app_label}.add_{org.Staff._meta.model_name}",
            f"{org.Staff._meta.app_label}.change_{org.Staff._meta.model_name}",
            # Units - Create & Update
            f"{org.Unit._meta.app_label}.add_{org.Unit._meta.model_name}",
            f"{org.Unit._meta.app_label}.change_{org.Unit._meta.model_name}",
            # Units - Department & Update
            f"{org.Department._meta.app_label}.add_{org.Department._meta.model_name}",
            f"{org.Department._meta.app_label}.change_{org.Department._meta.model_name}",
        ],
    }

    ANNUAL_PLAN_INITIATORS: dict[str, typing.Any] = {
        "name": "Annual Plan Initiators",
        "perms": [
            f"{org.AnnualPlan._meta.app_label}.add_{org.AnnualPlan._meta.model_name}",
            f"{org.AnnualPlan._meta.app_label}.change_{org.AnnualPlan._meta.model_name}",
            f"{org.DepartmentProcurementPlan._meta.app_label}.approve_{org.DepartmentProcurementPlan._meta.model_name}",
        ],
    }

    DEPARTMENT_BUDGET_PLANNERS: dict[str, typing.Any] = {
        "name": "Department Budget Planners",
        "perms": [
            f"{org.DepartmentProcurementPlan._meta.app_label}.add_{org.DepartmentProcurementPlan._meta.model_name}",
            f"{org.DepartmentProcurementPlan._meta.app_label}.change_{org.DepartmentProcurementPlan._meta.model_name}",
        ],
    }

    PROCUREMENT_APPROVERS: dict[str, typing.Any] = {
        "name": "Procurement Approvers",
        "perms": [
            f"{proc.RFQApproval._meta.app_label}.add_{proc.RFQApproval._meta.model_name}",
            f"{proc.RFQApproval._meta.app_label}.change_{proc.RFQApproval._meta.model_name}",
        ],
    }

    PROCUREMENT_COORDINATORS: dict[str, typing.Any] = {
        "name": "Procurement Coordinators",
        "perms": [
            f"{proc.RFQ._meta.app_label}.add_{proc.RFQ._meta.model_name}",
            f"{proc.RFQ._meta.app_label}.change_{proc.RFQ._meta.model_name}",
        ],
    }

    @classmethod
    def bootstrap_groups(cls):
        groups = (
            cls.STAFF_MEMBER,
            cls.SUPER_ADMIN,
            cls.ANNUAL_PLAN_INITIATORS,
            cls.DEPARTMENT_BUDGET_PLANNERS,
            cls.PROCUREMENT_APPROVERS,
            cls.PROCUREMENT_COORDINATORS,
        )

        return groups
