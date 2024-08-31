import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from APP_COMPANY import APP_COMPANY

from apps.procurement.models import RFQ, RFQApproval
from apps.core.utilities.text_choices import RFQLevelChoices, ApprovalChoices
from apps.core.processors.multithreading import MultiThreading


@receiver(post_save, sender=RFQ)
def create_quotation_from_rfq(created, instance: RFQ, *args, **kwargs):
    publish_levels = [RFQLevelChoices.PUBLISH_LEVEL.value, RFQLevelChoices.APPROVAL_LEVEL.value]
    if instance.published and (instance.level in publish_levels) and not instance.open_status:
        requires_gppa_approval = instance.requires_gppa_approval
        if requires_gppa_approval:
            approval_record:RFQApproval = instance.approval_record # type:ignore
            gppa_approval = approval_record.gppa_approval
            if not gppa_approval:
                RFQ.objects.filter(pk=instance.pk).update(editable = True)
                return
            if gppa_approval.approve == ApprovalChoices.REJECTED.value:
                RFQ.objects.filter(pk=instance.pk).update(editable = True)
                return
        RFQ.objects.filter(pk=instance.pk).update( open_status=True, level=RFQLevelChoices.QUOTATION_LEVEL.value, published=True)
        send_invitation_mails(instance)


def send_invitation_mails(rfq:RFQ):
    "Sends RFQ invitation mails to selected vendors"
    def mailer():
        for vendor in rfq.suppliers.all():
            context = {
                "vendor": vendor,
                "quotation": rfq,
                "platform": APP_COMPANY,
            }
            html = render_to_string("core/rfq_invitation.html", context=context)
            try:
                send_mail(
                    "RFQ Invitation",
                    "",
                    from_email=f"{APP_COMPANY["name"]} <{os.getenv("EMAIL_HOST_USER")}>",
                    fail_silently=False,
                    recipient_list=[vendor.contact_person.email],  # type: ignore
                    html_message=html,
                )
            except Exception as e:
                print("ERROR!  -->  [%s]" % e)
                print("[Error Mailing] --> ",vendor)
    thread = MultiThreading(target=mailer)
