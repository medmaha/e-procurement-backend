from django.urls import path

from .create import requisitions_create
from .detail import requisitions_detail
from .approve.create import approve_create
from .approve.detail import approve_detail
from .approve.list import approve_list

requisitions_url = [
    path("requisitions/create", requisitions_create, name="requisitions_create"),
    path("requisitions/<str:id>/", requisitions_detail, name="requisitions_detail"),
    path(
        "requisitions/approvals/list",
        approve_list,
        name="list_requisition_approval",
    ),
    path(
        "requisitions/approvals/<id>/create/",
        approve_create,
        name="create_requisition_approval",
    ),
    path(
        "requisitions/approvals/<id>/detail",
        approve_detail,
        name="detail_requisition_approval",
    ),
]
