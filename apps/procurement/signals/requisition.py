from decimal import Decimal
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from apps.procurement.models import Requisition, RequisitionItem, RequisitionApproval
from apps.organization.models.procurement_plan import Threshold


@receiver(post_save, sender=RequisitionItem)
def update_requisition_items(created, instance: RequisitionItem, *args, **kwargs):
    if created:
        instance.description = instance.description.capitalize()
        instance.save()


@receiver(post_save, sender=Requisition)
def created_requisition_approval(created, instance: Requisition, *args, **kwargs):
    if created:
        instance.remarks = (instance.remarks or "").capitalize()

        RequisitionApproval.objects.create(
            requisition=instance,
            procurement_method="not_applied",
        )


@receiver(m2m_changed, sender=Requisition)
def do_something_with_many_to_many(sender, instance: Requisition, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        value = 0
        for item in instance.items.all():
            value += item.total_cost

        matching_threshold = Threshold.objects.filter(
            min_amount__lte=value, max_amount__gte=value
        ).first()

        if matching_threshold:
            approval, _ = RequisitionApproval.objects.get_or_create(
                requisition=instance
            )
            if matching_threshold.procurement_method:
                approval.procurement_method = matching_threshold.procurement_method
            approval.save()
