from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.procurement.models.rfq_approval import RFQApproval
from apps.core.utilities.text_choices import (
    RFQLevelChoices,
    ApprovalChoices,
    ApprovalChoices,
)


@receiver(post_save, sender=RFQApproval)
def update_rfq_status(created, instance: RFQApproval, *args, **kwargs):
    status = instance.approve
    instance.rfq.level = RFQLevelChoices.APPROVAL_LEVEL
    if status == ApprovalChoices.APPROVED.value:
        instance.rfq.approval_status = ApprovalChoices.APPROVED
        requires_approval = instance.rfq.requires_gppa_approval
        if requires_approval and instance.gppa_approval:
            instance.rfq.published = instance.rfq.auto_publish
            instance.rfq.level = RFQLevelChoices.PUBLISH_LEVEL
        elif not requires_approval:
            instance.rfq.published = instance.rfq.auto_publish
            instance.rfq.level = RFQLevelChoices.PUBLISH_LEVEL
        instance.rfq.open_status = False
    if status == ApprovalChoices.REJECTED.value:
        instance.rfq.approval_status = ApprovalChoices.REJECTED
        instance.rfq.published = False
        instance.rfq.open_status = False
    RFQApproval.objects.filter(id=instance.pk).update(editable=False)
    instance.rfq.save()
