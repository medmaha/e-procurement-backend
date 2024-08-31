from django.urls import path


# Annual Plan
from .views.annual_plans.create import AnnuaLPlanCreateView
from .views.annual_plans.approve import AnnualPlanApprovalView
from .views.annual_plans.retrieve import AnnualPlanRetrieveView
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
from .views.departments.retrieve import DepartmentRetrieveView

# Units
from .views.units.list import UnitListView
from .views.units.create import UnitsCreateView
from .views.units.update import UnitsUpdateView
from .views.units.select import UnitSelectionView
from .views.units.retrieve import UnitsRetrieveView, UnitsRetrieveUpdateView

# Staffs
from .views.staffs.list import StaffListView
from .views.staffs.create import StaffCreateView
from .views.staffs.update import StaffUpdateView
from .views.staffs.select import StaffSelectionView
from .views.staffs.retrieve import StaffRetrieveView, StaffUpdateRetrieveView


# referenced like --> /api/organization/*
urlpatterns = [
    # Annual Procurement Plans
    path("plans/thresholds/", ProcurementMethodThresholdView.as_view()),
    path("annual-plan/create/", AnnuaLPlanCreateView.as_view()),
    path("annual-plan/current/", AnnualPlanRetrieveView.as_view()),
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
    path("departments/<id>/", DepartmentRetrieveView.as_view()),
    path("departments/", DepartmentListView.as_view()),
    #
    # Units
    path("units/create/", UnitsCreateView.as_view()),
    path("units/update/", UnitsUpdateView.as_view()),
    path("units/select/", UnitSelectionView.as_view()),
    path("units/<id>/", UnitsRetrieveView.as_view()),
    path("units/", UnitListView.as_view()),
    path("units/retrieve/<id>/", UnitsRetrieveUpdateView.as_view()),
    #
    # Staffs
    path("staffs/create/", StaffCreateView.as_view()),
    path("staffs/update/", StaffUpdateView.as_view()),
    path("staffs/select/", StaffSelectionView.as_view()),
    path("staffs/<id>/", StaffRetrieveView.as_view()),
    path("staffs/", StaffListView.as_view()),
    path("staffs/retrieve/<id>/", StaffUpdateRetrieveView.as_view()),
]
