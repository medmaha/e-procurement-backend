from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.organization.models import Staff, Unit, Department
from apps.procurement.models.pr_approval_deligation import Delegation
from apps.procurement.models.pr_approval_matrix import ApprovalMatrix
from apps.procurement.models.requisition import Requisition, ApprovalChoices


def get_current_approver(requisition: Requisition):
    """
    Get the current approver for a requisition, considering delegations.
    """
    current_step = requisition.current_approval_step
    if not current_step:
        return None

    role = current_step.role
    department = requisition.officer_department

    # Check for active delegations
    delegations = Delegation.objects.filter(
        delegator__job_title=role,
        delegator__unit__department=department,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
    )

    if delegations.exists():
        delegation = delegations.first()
        if not delegation:
            return None
        return delegation.delegate

    return Staff.objects.filter(job_title=role, unit__department=department).first()


def get_matrix_for_requisition(requisition: Requisition):
    """
    Get the first matching approval matrix for a requisition.
    """
    # TODO: Fix the ordering style
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            return matrix
    return None  # Handle no matches found (e.g., assign default workflow)


def get_workflow_for_requisition(requisition: Requisition):
    """
    Get the first matching workflow for a requisition.
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            return matrix.workflow
    return None  # Handle no matches found (e.g., assign default workflow)


def get_workflow_list_for_requisition(requisition: Requisition):
    """
    Get a list of all matching workflows for a requisition.
    """
    workflows = ApprovalMatrix.objects.all()  # Get all matrix entries
    _workflows = []
    for matrix in workflows:
        if matrix.matches_requisition(requisition):
            _workflows.append(matrix.workflow)
    return _workflows


def get_matrixes_for_requisition(requisition: Requisition):
    """
    Get a list of all matching approval matrices for a requisition.
    """
    matrices = ApprovalMatrix.objects.all()  # Get all matrix entries
    _matrices = []
    for matrix in matrices:
        if matrix.matches_requisition(requisition):
            _matrices.append(matrix)
    return _matrices
