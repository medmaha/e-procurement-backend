from django.urls import path

from .views.plans.list import ProcurementPlanListView

# Requisition
from .views.requisitions.create import RequisitionCreateView
from .views.requisitions.update import RequisitionUpdateView
from .views.requisitions.retrieve import RequisitionRetrieveView
from .views.requisitions.list import RequisitionListView, RequisitionSelectView
from .views.requisitions.approval import RequisitionApprovalView

# - Workflow Approval Steps
from .views.requisitions.workflows import (
    RequisitionWorkflowAPIView,
    RequisitionApprovalStepAPIView,
    RequisitionApprovalMatrixAPIView,
)

# RFQ
from .views.rfq.list import RfqListView, RfqSelectView
from .views.rfq.update import RFUpdateView
from .views.rfq.create import RFQCreateView
from .views.rfq.approve import RFQApprovalView
from .views.rfq.retrieve import RfqRetrieveView
from .views.rfq.opened_by import RfqOpenedByView

# RFQ Response
from .views.rfq.responses.list import (
    QuotationRespondListView,
    QuotationRespondSelectView,
)

# RFQ Evaluation
from .views.rfq.evaluation.create import RFQEvaluationCreateView
from .views.rfq.evaluation.remove import RFQEvaluationRemoveView
from .views.rfq.evaluation.retrieve import RFQEvaluationRetrieveView

from .views.rfq.responses.reject import QuotationRespondRejectView
from .views.rfq.responses.retrieve import QuotationRespondRetrieveView

# RFQ Contract
from .views.rfq.contract.create import CreateContract
from .views.rfq.contract.list import RFQContractListView
from .views.rfq.contract.approve import ContractApprovalCreateAPIView
from .views.rfq.contract.negotiations import (
    RFQNegotiationView,
)

# RFQ Purchase Order
from .views.purchase_order.list import PurchaseOrderListView
from .views.purchase_order.create import PurchaseOrderCreateView
from .views.purchase_order.retrieve import PurchaseOrderRetrieveView
from .views.purchase_order.approve import PurchaseOrderApproveView
from .views.purchase_order.reject import PurchaseOrderRejectView

#

from .views.form101.view import Form101RetrieveView

# reference /api/procurement/*
urlpatterns = [
    path("list", ProcurementPlanListView.as_view()),
    #
    # Requisition
    path("form101/retrieve/", Form101RetrieveView.as_view()),
    path("requisitions/select/", RequisitionSelectView.as_view()),
    path("requisitions/approve/", RequisitionApprovalView.as_view()),
    path("requisitions/create/", RequisitionCreateView.as_view()),
    path("requisitions/update/", RequisitionUpdateView.as_view()),
    path("requisitions/list", RequisitionListView.as_view()),
    # ---- workflows ----
    path(
        "requisitions/workflows/matrices/",
        RequisitionApprovalMatrixAPIView.as_view(),
    ),
    path(
        "requisitions/workflows/matrices/<matrix_id>/",
        RequisitionApprovalMatrixAPIView.as_view(),
    ),
    path(
        "requisitions/workflows/steps/",
        RequisitionApprovalStepAPIView.as_view(),
    ),
    path(
        "requisitions/workflows/steps/<approval_step_id>/",
        RequisitionApprovalStepAPIView.as_view(),
    ),
    path(
        "requisitions/workflows/approval-steps/",
        RequisitionApprovalStepAPIView.as_view(),
    ),
    path(
        "requisitions/workflows/approval-steps/<approval_step_id>/",
        RequisitionApprovalStepAPIView.as_view(),
    ),
    path("requisitions/workflows/", RequisitionWorkflowAPIView.as_view()),
    path(
        "requisitions/workflows/<workflow_id>/",
        RequisitionWorkflowAPIView.as_view(),
    ),
    # ---- workflows ----
    path("requisitions/<slug>/", RequisitionRetrieveView.as_view()),
    path("requisitions/", RequisitionListView.as_view()),
    #
    # RFQ Responses
    path("rfq/responses/select/", QuotationRespondSelectView.as_view()),
    path("rfq/responses/reject/", QuotationRespondRejectView.as_view()),
    path("rfq/responses/list/", QuotationRespondListView.as_view()),
    path("rfq/responses/<slug>/", QuotationRespondRetrieveView.as_view()),
    #
    # RFQ Evaluation
    path("rfq/evaluation/create/", RFQEvaluationCreateView.as_view()),
    path("rfq/evaluation/remove/", RFQEvaluationRemoveView.as_view()),
    path("rfq/evaluation/retrieve/<rfq_id>/", RFQEvaluationRetrieveView.as_view()),
    #
    # RFQ Contracts
    path("rfq/contracts/negotiations/list/", RFQNegotiationView.as_view()),
    path("rfq/contracts/negotiations/<contract_id>/", RFQNegotiationView.as_view()),
    path("rfq/contracts/negotiations/", RFQNegotiationView.as_view()),  # CRUD Handlers
    path("rfq/contracts/list/", RFQContractListView.as_view()),
    path("rfq/contracts/create/", CreateContract.as_view()),
    path("rfq/contracts/create/", CreateContract.as_view()),
    path("rfq/contracts/", RFQContractListView.as_view()),
    path(
        "rfq/contracts/<contract_id>/approval/", ContractApprovalCreateAPIView.as_view()
    ),
    #
    # RFQ
    path("rfq/select/", RfqSelectView.as_view()),
    path("rfq/create/", RFQCreateView.as_view()),
    path("rfq/update/", RFUpdateView.as_view()),
    path("rfq/approve/", RFQApprovalView.as_view()),
    path("rfq/publish/", RFQApprovalView.as_view()),
    path("rfq/list/", RfqListView.as_view()),
    path("rfq/opened-by/", RfqOpenedByView.as_view()),
    path("rfq/opened-by/<rfq_id>/", RfqOpenedByView.as_view()),
    path("rfq/<slug>/", RfqRetrieveView.as_view()),
    path("rfq/", RfqListView.as_view()),
    #
    # Purchase Orders
    path("quotations/respond/select/", QuotationRespondSelectView.as_view()),
    path("quotations/respond/reject/", QuotationRespondRejectView.as_view()),
    path("quotations/respond/retrieve/<id>/", QuotationRespondRetrieveView.as_view()),
    path("quotations/respond/", QuotationRespondListView.as_view()),
    #
    path("purchase-orders/retrieve/<id>/", PurchaseOrderRetrieveView.as_view()),
    path("purchase-orders/create/", PurchaseOrderCreateView.as_view()),
    path("purchase-orders/approve/", PurchaseOrderApproveView.as_view()),
    path("purchase-orders/reject/", PurchaseOrderRejectView.as_view()),
    path("purchase-orders/list", PurchaseOrderListView.as_view()),
    path("purchase-orders/", PurchaseOrderListView.as_view()),
]
