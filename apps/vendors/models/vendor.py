import os
import uuid
from threading import Thread
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from apps.core.utilities.generators import generate_unique_id
from apps.accounts.models import Account
from apps.organization.models import Company


def upload_to(instance, filename: str):
    path = f"vendors/id_{instance.id}/logo/{filename}"
    return path


def upload_company_logo(instance, filename: str):
    path = f"vendors/id_{instance.pk}/logo/{filename}"
    return path


def upload_company_certificates(instance, filename: str):
    path = f"vendors/id_{instance.vendor.pk}/certificates/{filename}"
    return path


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        Company,
        unique=False,
        on_delete=models.CASCADE,
        related_name="vendor_company",
    )

    active = models.BooleanField(default=False, null=True, blank=True)

    user_account = models.ForeignKey(
        Account,
        blank=True,
        on_delete=models.CASCADE,
        related_name="vendor_account",
    )

    verified = models.BooleanField(default=False, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def slug(self):
        return id

    def __str__(self):
        return self.company.name

    @property
    def name(self):
        return self.company.name

    class Meta:
        verbose_name = "Vendor"
        ordering = ["-created_date", "-last_modified", "verified", "active"]

    @property
    def unique_id(self):
        return generate_unique_id("V", self.pk, 6)

    def send_activation_mail(self, v_code: str | None = None, activation=None):
        def mailer():
            context = {
                "code__": v_code,
                "company": self.company.name,
                "activated": self.active if activation is None else activation,
                "recipient": self.user_account.full_name,  # type: ignore
            }
            html = render_to_string("vendors/activation_mail.html", context=context)
            try:
                send_mail(
                    "Account Activation",
                    "",
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    fail_silently=False,
                    recipient_list=[self.user_account.email],  # type: ignore
                    html_message=html,
                )
            except Exception as e:
                print("ERROR!   --->   [%s]" % e)

        thread = Thread(target=mailer)
        thread.start()

    def self_invitation_mail(self, quotation):
        def mailer():
            context = {
                "vendor": self,
                "quotation": quotation,
                "organization": self.company.name,
            }
            html = render_to_string("vendors/rfq_invitation_mail.html", context=context)
            try:
                send_mail(
                    "RFQ Invitation",
                    "",
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    fail_silently=False,
                    recipient_list=[self.user_account.email],  # type: ignore
                    html_message=html,
                )
            except Exception as e:
                print("ERROR!   --->   [%s]" % e)

        thread = Thread(target=mailer)
        thread.start()
