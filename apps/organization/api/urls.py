from django.urls import path


# Company
from .views.company.get import CompanyGetAPIView
from .views.company.put import CompanyUpdateAPIView
from .views.company.list import CompanyListAPIView
from .views.company.query import CompanyQueryAPIView
from .views.company.post import CompanyCreateAPIView
from .views.company.delete import CompanyDisableAPIView


# Annual Plan
from .views.annual_plans.create import AnnuaLPlanCreateView
from .views.annual_plans.approve import AnnualPlanApprovalView
from .views.annual_plans.retrieve import AnnualPlanGetAPIView
from .views.annual_plans.threshold import ProcurementMethodThresholdView
from .views.annual_plans.request_4_approval import AnnualPlanRequestForApprovalView

# Department Plan
from .views.annual_plans.department_plans.list import DepartmentProcurementPlanListView
from .views.annual_plans.department_plans.create import (
    DepartmentProcurementPlanCreateView,
)
from .views.annual_plans.department_plans.select import (
    DepartmentProcurementPlansSelectView,
)

# Departments
from .views.departments.list import DepartmentListView
from .views.departments.create import DepartmentCreateView
from .views.departments.update import DepartmentUpdateView
from .views.departments.select import DepartmentSelectionView
from .views.departments.retrieve import DepartmentGetAPIView

# Units
from .views.units.list import UnitListView
from .views.units.create import UnitsCreateView
from .views.units.update import UnitsUpdateView
from .views.units.select import UnitSelectionView
from .views.units.retrieve import UnitsGetAPIView, UnitsRetrieveUpdateView

# Staffs
from .views.staffs.get import StaffGetAPIView
from .views.staffs.put import StaffUpdateAPIView
from .views.staffs.list import StaffListAPIView
from .views.staffs.post import StaffCreateAPIView
from .views.staffs.query import StaffQueryAPIView
from .views.staffs.delete import StaffDisableAPIView


# referenced like --> /api/organization/*
urlpatterns = [
    # Company
    path("company/", CompanyListAPIView.as_view()),
    path("company/query/", CompanyQueryAPIView.as_view()),
    path("company/create/", CompanyCreateAPIView.as_view()),
    path("company/<slug>/", CompanyGetAPIView.as_view()),
    path("company/<slug>/update/", CompanyUpdateAPIView.as_view()),
    path("company/<slug>/disable/", CompanyDisableAPIView.as_view()),
    #
    # Annual Procurement Plans
    path("plans/thresholds/", ProcurementMethodThresholdView.as_view()),
    path("annual-plan/create/", AnnuaLPlanCreateView.as_view()),
    path("annual-plan/current/", AnnualPlanGetAPIView.as_view()),
    path("annual-plan/approval/", AnnualPlanApprovalView.as_view()),
    path("annual-plan/approval/request/", AnnualPlanRequestForApprovalView.as_view()),
    #
    # Departmental Procurement Plans
    path(
        "annual-plan/departmental/list/",
        DepartmentProcurementPlanListView.as_view(),
    ),
    path(
        "annual-plan/departmental/create/",
        DepartmentProcurementPlanCreateView.as_view(),
    ),
    path(
        "annual-plan/departmental/select/",
        DepartmentProcurementPlansSelectView.as_view(),
    ),
    # Departments
    path("departments/create/", DepartmentCreateView.as_view()),
    path("departments/update/", DepartmentUpdateView.as_view()),
    path("departments/select/", DepartmentSelectionView.as_view()),
    path("departments/<id>/", DepartmentGetAPIView.as_view()),
    path("departments/", DepartmentListView.as_view()),
    #
    # Units
    path("units/create/", UnitsCreateView.as_view()),
    path("units/update/", UnitsUpdateView.as_view()),
    path("units/select/", UnitSelectionView.as_view()),
    path("units/<id>/", UnitsGetAPIView.as_view()),
    path("units/", UnitListView.as_view()),
    path("units/retrieve/<id>/", UnitsRetrieveUpdateView.as_view()),
    #
    # Staffs
    path("staffs/", StaffListAPIView.as_view()),
    path("staffs/create/", StaffCreateAPIView.as_view()),
    path("staffs/query/", StaffQueryAPIView.as_view()),
    path("staffs/<staff_id>/", StaffGetAPIView.as_view()),
    path("staffs/<staff_id>/update/", StaffUpdateAPIView.as_view()),
    path("staffs/<staff_id>/disable/", StaffDisableAPIView.as_view()),
]
