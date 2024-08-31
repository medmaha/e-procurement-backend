from threading import Thread
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from apps.procurement.models import RequisitionApproval

from apps.core.utilities.text_choices import ApprovalChoices, ApprovalChoices


@receiver(post_save, sender=RequisitionApproval)
def update_approval(created, instance: RequisitionApproval, *args, **kwargs):
    if not created:
        rejected = False
        status = ApprovalChoices.PENDING.value
        if instance.unit_approval:
            rejected = instance.unit_approval.approve == ApprovalChoices.REJECTED.value
        if instance.department_approval:
            rejected = (
                instance.department_approval.approve == ApprovalChoices.REJECTED.value
            )
        if instance.procurement_approval:
            rejected = (
                instance.procurement_approval.approve == ApprovalChoices.REJECTED.value
            )
        if instance.finance_approval:
            rejected = (
                instance.finance_approval.approve == ApprovalChoices.REJECTED.value
            )
            status = ApprovalChoices.ACCEPTED.value

        RequisitionApproval.objects.filter(pk=instance.pk).update(
            editable=False,
            status=(ApprovalChoices.REJECTED.value if rejected else status),
        )
