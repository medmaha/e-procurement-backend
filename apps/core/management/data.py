from datetime import datetime
import random

from apps.organization.models import (
    DepartmentProcurementPlan,
    PlanItem,
    AnnualPlan,
    Department,
    Unit,
    Staff,
)


DEPARTMENTS = [
    {
        "name": "Admin Department",
        "description": "Responsible for administrative tasks and office management.",
        "phone": "+220 123 4567",
        "email": "admin.department@mail.com",
    },
    {
        "name": "IT Support Department",
        "description": "Provides technical support and resolves IT-related issues for employees and clients.",
        "phone": "+220 234 5678",
        "email": "support@mail.com",
    },
    {
        "name": "Software Development Department",
        "description": "Designs, develops, and maintains software solutions.",
        "phone": "+220 345 6789",
        "email": "devteam@mail.com",
    },
    {
        "name": "Quality Assurance (QA) Department",
        "description": "Ensures the quality of software and systems through testing and validation.",
        "phone": "+220 456 7890",
        "email": "qa@mail.com",
    },
    {
        "name": "Sales and Marketing Department",
        "description": "Responsible for promoting and selling ICT solutions to clients.",
        "phone": "+220 567 8901",
        "email": "sales@mail.com",
    },
    {
        "name": "Project Management Office (PMO)",
        "description": "Manages projects, coordinates teams, and ensures project delivery.",
        "phone": "+220 678 9012",
        "email": "pmo@mail.com",
    },
    {
        "name": "Procurement Department",
        "description": "Manages procurement processes and vendor relations.",
        "phone": "+220 789 0123",
        "email": "procurement@mail.com",
    },
    {
        "name": "Finance Department",
        "description": "Handles financial operations",
        "phone": "+220 123 4567",
        "email": "finance@mail.com",
    },
]


def generate_departments():
    for data in DEPARTMENTS:
        Department.objects.create(**data)
    print("✅Departments generated successfully\n")


UNITS = [
    {
        "name": "Office Management Unit",
        "department_id": 1,  # Associated with Admin Department
        "description": "Handles office logistics and administrative tasks.",
        "phone": "+220 123 4567",
        # "email": "office.management@mail.com",
    },
    {
        "name": "HR and Recruitment Unit",
        "department_id": 1,  # Associated with Admin Department
        "description": "Manages human resources and recruitment processes.",
        "phone": "+220 987 6543",
        # "email": "hr.recruitment@mail.com",
    },
    {
        "name": "Technical Support Unit",
        "department_id": 2,  # Associated with IT Support Department
        "description": "Provides frontline technical assistance to employees and clients.",
        "phone": "+220 234 5678",
        # "email": "tech.support@mail.com",
    },
    {
        "name": "Infrastructure Maintenance Unit",
        "department_id": 2,  # Associated with IT Support Department
        "description": "Manages and maintains IT infrastructure and systems.",
        "phone": "+220 345 6789",
        # "email": "infrastructure@mail.com",
    },
    {
        "name": "Software Development Team",
        "department_id": 3,  # Associated with Software Development Department
        "description": "Develops software solutions as per project requirements.",
        "phone": "+220 456 7890",
        # "email": "devteam@mail.com",
    },
    {
        "name": "Quality Assurance Unit",
        "department_id": 3,  # Associated with Software Development Department
        "description": "Conducts quality checks and ensures software quality.",
        "phone": "+220 567 8901",
        # "email": "qa@mail.com",
    },
    {
        "name": "Operations Unit",
        "department_id": 4,  # Associated with Sales and Marketing Department
        "description": "Manages sales operations.",
        "phone": "+220 678 9012",
        # "email": "sales.unit1@mail.com",
    },
    {
        "name": "Customer Relations Unit",
        "department_id": 4,  # Associated with Sales and Marketing Department
        "description": "Handles customer relations.",
        "phone": "+220 789 0123",
        # "email": "sales.unit2@mail.com",
    },
    {
        "name": "Coordination Unit",
        "department_id": 5,  # Associated with Project Management Office
        "description": "Coordinates project activities.",
        "phone": "+220 890 1234",
        # "email": "pmo.unit1@mail.com",
    },
    {
        "name": "Resource Management Unit",
        "department_id": 5,  # Associated with Project Management Office
        "description": "Manages project resources.",
        "phone": "+220 901 2345",
        # "email": "pmo.unit2@mail.com",
    },
    {
        "name": "Process Management Unit",
        "department_id": 6,  # Associated with Procurement Department
        "description": "Manages procurement processes.",
        "phone": "+220 912 3456",
        # "email": "procurement.unit1@mail.com",
    },
    {
        "name": "Vendor Relations Unit",
        "department_id": 6,  # Associated with Procurement Department
        "description": "Handles vendor relations.",
        "phone": "+220 923 4567",
        # "email": "procurement.unit2@mail.com",
    },
    {
        "name": f"Finance Unit",
        "department_id": 7,
        "description": f"Unit of Finance Department",
        "phone": "+220 123 4567",
        # "email": f"finance.unit@company.com",
    }
    # Add more units or modify details as needed...
]


def generate_units():
    for unit in UNITS:
        Unit.objects.create(**unit)
    print("✅Units generated successfully\n")


STAFFS = [
    {
        "first_name": "System",
        "middle_name": "",
        "last_name": "Admin",
        "unit_id": 1,  # Associated with Admin Unit
        "biography": "Responsible for administrative tasks.",
        "job_title": "Administrator",
        "phone": "+220 123 4567",
        "disabled": False,
        "email": "admin@mail.com",
        "gender": "male",
    },
   
    {
        "first_name": "Staff",
        "middle_name": "",
        "last_name": "Staff",
        "unit_id": 5,  # Associated with Software Development Unit 1
        "biography": "Develops software solutions.",
        "job_title": "Software Developer",
        "phone": "+220 345 6789",
        "disabled": False,
        "email": "staff@mail.com",
    },
    {
        "first_name": "Unit",
        "middle_name": "",
        "last_name": "Head",
        "unit_id": 7,  # Associated with Sales Department - Operations Management Unit
        "biography": "Manages units operations.",
        "job_title": "Unit Operations Manager",
        "phone": "+220 456 7890",
        "disabled": False,
        "email": "unit@mail.com",
    },
    {
        "first_name": "Department",
        "middle_name": "",
        "last_name": "Head",
        "unit_id": 7,  # Associated with Project Management Department - Coordination Unit
        "biography": "Coordinates project activities.",
        "job_title": "Department Manager",
        "phone": "+220 567 8901",
        "disabled": False,
        "email": "department@mail.com",
    },
    {
        "first_name": "Procurement",
        "middle_name": "",
        "last_name": "Officer",
        "unit_id": 11,  # Associated with Procurement Department - Process Management Unit
        "biography": "Manages procurement processes.",
        "job_title": "Procurement Manager",
        "phone": "+220 678 9012",
        "disabled": False,
        "email": "procurement@mail.com",
    },
    {
        "first_name": "Finance",
        "middle_name": "",
        "last_name": "Officer",
        "unit_id": 11,  # Associated with Procurement Department - Process Management Unit
        "biography": "Manages financial processes.",
        "job_title": "Accountant",
        "phone": "+220 678 9012",
        "disabled": False,
        "email": "finance@mail.com",
    },
    # Add more staff members and assign them to the corresponding units...
]


def generate_staffs():
    for staff in STAFFS:
        Staff(**staff).save()

    print("✅Staffs generated successfully\n")


# Generate Procurement Plans data dynamically
def generate_annual_plans():
    departments_data = Department.objects.all()
    procurement_plans_data = []
    for department in departments_data:
        plan_data = {
            "department": department,
            "description": random.choice([f"Procurement plan for {department.name}", f"{department.name} Procurement plan"]),
        }
        procurement_plans_data.append(DepartmentProcurementPlan.objects.create(**plan_data))

    # Generate Plan Items data dynamically
    plan_items_data = []
    for i, plan in enumerate(procurement_plans_data, start=1):
        for _ in range(random.randint(1, 4)):
            item_data = {
                "plan": plan,
                "description": f"{random.choice(["Item", "Service"])} {random.randint(1, 100)} for {departments_data[i-1].name}",
                "quantity": random.randint(50, 500),
                "budget": random.randint(10000, 100000),
                "measurement_unit": random.choice(["units", "pieces", "bytes", "bundles", "metres"]),
                "quarter_1_budget": random.randint(4000, 10000),
                "quarter_2_budget": random.randint(4000, 10000),
                "quarter_3_budget": random.randint(4000, 10000),
                "quarter_4_budget": random.randint(4000, 10000),
            }
            plan_items_data.append(PlanItem.objects.create(**item_data))

    # Generate Annual Procurement Plan data dynamically
    start_year = 2020
    end_year = 2024
    for year in range(start_year, end_year + 1):
        annual_data = {
            "title": f"Annual Procurement Plan - Year {year}",
            "description": f"Annual procurement plan for the year {year}",
            "year_start": datetime(year, 1, 1),
            "renewed_year": None,
            "org_approved": None,
            "gppa_approved": None,
            "is_operational": None,
            "is_invalid": None,
        }

        annual = AnnualPlan.objects.create(**annual_data)
        plan_ids = list(range(1, len(departments_data) + 1))
        random.shuffle(plan_ids)
        plans = DepartmentProcurementPlan.objects.filter(pk__in=plan_ids)
        selected_plans = plans[: random.randint(1, len(plan_ids))]
        annual.department_plans.set(selected_plans)
    print("✅Annual Procurement plans generated successfully\n")
