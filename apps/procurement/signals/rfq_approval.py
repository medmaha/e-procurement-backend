from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.procurement.models import RFQ, RFQApproval
from apps.core.utilities.text_choices import (
    RFQLevelChoices,
    ApprovalChoices,
    ApprovalChoices,
)


@receiver(post_save, sender=RFQApproval)
def update_rfq_status(created, instance: RFQApproval, *args, **kwargs):
    """
    Updates the status of the RFQ based on the approval status of the RFQApproval
    """

    if not created:
        return

    status = instance.approve
    rfq = instance.rfq

    # if the approval is approved and the RFQ requires GPPA approval, update the level to publish level
    if status == ApprovalChoices.APPROVED.value:
        rfq.approval_status = ApprovalChoices.APPROVED
        if rfq.auto_publish:
            rfq.published = True
            rfq.level = RFQLevelChoices.QUOTATION_LEVEL
        else:
            rfq.published = False
            rfq.level = RFQLevelChoices.PUBLISH_LEVEL
    else:
        rfq.approval_status = instance.approve

    rfq.approval_status = instance.approve
    rfq.save()


def notify_vendors_for_rfq(rfq: RFQ):

    for supplier in rfq.suppliers.all():
        print(
            f"""
        Dear {supplier.name},

        You've been selected to quote for the RFQ (RFQ0000{rfq.pk}).

        please login to your account to view the details.\n
    """
        )
