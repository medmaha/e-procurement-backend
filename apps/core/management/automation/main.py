# ... existing code ...

from django.db import transaction
from apps.organization.models import Department, Staff, Unit
from apps.procurement.models import ApprovalMatrix, ApprovalStep, ApprovalWorkflow
from apps.accounts.models import Account
from backend.apps.procurement.models.requisition_approval_workflow import WorkflowStep


@transaction.atomic
def create_sample_workflows_and_matrices():
    # Create departments
    finance_dept = Department.objects.create(name="Finance", email="finance@prc.gm")
    it_dept = Department.objects.create(
        name="Information Technology", email="it@prc.gm"
    )
    hr_dept = Department.objects.create(name="Human Resources", email="hr@prc.gm")
    management_dept = Department.objects.create(
        name="Management", email="management@prc.gm"
    )

    # Create units
    finance_unit = Unit.objects.create(name="Finance Unit", department=finance_dept)
    it_unit = Unit.objects.create(name="IT Unit", department=it_dept)
    hr_unit = Unit.objects.create(name="HR Unit", department=hr_dept)
    management_unit = Unit.objects.create(
        name="Management Unit", department=management_dept
    )

    # Create staff
    def create_staff(email, first_name, last_name, unit, job_title):
        account = Account.objects.create(email=email, username=email)
        return Staff.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            unit=unit,
            job_title=job_title,
            user_account=account,
            disabled=False,
        )

    ceo = create_staff(
        "modou.drammeh@prc.gm",
        "Modou Lamin",
        "Drammeh",
        management_unit,
        "Chief Executive Officer",
    )
    cfo = create_staff(
        "muhammed.sillah@prc.gm",
        "Muhammed",
        "Sillah",
        finance_unit,
        "Chief Financial Officer",
    )
    hr_manager = create_staff(
        "jainaba.faal@prc.gm", "Jainaba", "Faal", hr_unit, "HR Manager"
    )
    finance_manager = create_staff(
        "ousman.ndure@prc.gm", "Ousman", "Ndure", finance_unit, "Finance Manager"
    )
    cio = create_staff(
        "mahammed.touray@prc.gm",
        "Mahammed",
        "Touray",
        it_unit,
        "Chief Information Officer",
    )
    it_manager = create_staff(
        "mahammed.darboe@prc.gm", "Mahammed", "Darboe", it_unit, "IT Manager"
    )

    # Create workflows and matrices
    workflows_and_matrices = [
        {
            "name": "IT Equipment Purchase (Low Value)",
            "steps": [
                {"name": "IT Manager Approval", "role": "IT Manager", "order": 1},
                {
                    "name": "CIO Approval",
                    "role": "Chief Information Officer",
                    "order": 2,
                    "is_final": True,
                },
            ],
            "matrix": {"min_amount": 0, "max_amount": 50000, "department": it_dept},
        },
        {
            "name": "IT Equipment Purchase (High Value)",
            "steps": [
                {"name": "IT Manager Approval", "role": "IT Manager", "order": 1},
                {
                    "name": "CIO Approval",
                    "role": "Chief Information Officer",
                    "order": 2,
                },
                {
                    "name": "CFO Approval",
                    "role": "Chief Financial Officer",
                    "order": 3,
                    "is_final": True,
                },
            ],
            "matrix": {"min_amount": 50001, "max_amount": None, "department": it_dept},
        },
        {
            "name": "Office Supplies Purchase",
            "steps": [
                {
                    "name": "Finance Manager Approval",
                    "officer": finance_manager,
                    "order": 1,
                    "is_final": True,
                },
            ],
            "matrix": {
                "min_amount": 0,
                "max_amount": 10000,
                "department": finance_dept,
            },
        },
        {
            "name": "Capital Expenditure",
            "steps": [
                {
                    "name": "Finance Manager Approval",
                    "officer": finance_manager,
                    "order": 1,
                },
                {"name": "CFO Approval", "officer": cfo, "order": 2},
                {"name": "CEO Approval", "officer": ceo, "order": 3, "is_final": True},
            ],
            "matrix": {
                "min_amount": 100000,
                "max_amount": None,
                "department": finance_dept,
            },
        },
        {
            "name": "HR-related Purchases",
            "steps": [
                {"name": "HR Manager Approval", "officer": hr_manager, "order": 1},
                {"name": "CFO Approval", "officer": cfo, "order": 2, "is_final": True},
            ],
            "matrix": {"min_amount": 0, "max_amount": None, "department": hr_dept},
        },
        {
            "name": "Cross-department Purchase (Low Value)",
            "steps": [
                {"name": "Department Manager Approval", "officer": None, "order": 1},
                {
                    "name": "Finance Manager Approval",
                    "officer": finance_manager,
                    "order": 2,
                    "is_final": True,
                },
            ],
            "matrix": {"min_amount": 0, "max_amount": 25000},
        },
        {
            "name": "Cross-department Purchase (High Value)",
            "steps": [
                {"name": "Department Manager Approval", "officer": None, "order": 1},
                {
                    "name": "Finance Manager Approval",
                    "officer": finance_manager,
                    "order": 2,
                },
                {"name": "CFO Approval", "officer": cfo, "order": 3},
                {"name": "CEO Approval", "officer": ceo, "order": 4, "is_final": True},
            ],
            "matrix": {"min_amount": 25001, "max_amount": None},
        },
    ]

    for wf_data in workflows_and_matrices:
        # Create workflow
        workflow = ApprovalWorkflow.objects.create(name=wf_data["name"])

        # Create steps
        for step_data in wf_data["steps"]:
            step = ApprovalStep.objects.create(
                name=step_data["name"],
                role=step_data["role"],
                order=step_data["order"],
                is_final=step_data.get("is_final", False),
                department=wf_data["matrix"].get("department"),
            )
            WorkflowStep.objects.create(
                workflow=workflow,
                step=step,
                order=step_data["order"],
            )

        # Create matrix
        ApprovalMatrix.objects.create(
            workflow=workflow,
            min_amount=wf_data["matrix"].get("min_amount"),
            max_amount=wf_data["matrix"].get("max_amount"),
            department=wf_data["matrix"].get("department"),
            unit=wf_data["matrix"].get("unit"),
        )

    print("\n\n✅ Sample workflows and matrices created successfully.\n\n")
