from apps.procurement.models import (
    RequisitionItem,
)
from . import rfq
from . import rfq_contract
from . import requisition
from . import requisition_approval

# from . import approvals


from django.contrib import admin


admin.site.register(requisition.Requisition, requisition.RequisitionAdmin, index=3)
admin.site.register(RequisitionItem)
admin.site.register(
    requisition_approval.RequisitionApproval,
    requisition_approval.RequisitionApprovalAdmin,
    index=4,
)

admin.site.register(rfq.RFQ, rfq.RFQAdmin, index=5)


from apps.procurement.admin import approvals
