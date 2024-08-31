import os
from threading import Thread
from django.db import models
from django.utils.text import slugify
from apps.accounts.models import Account
from apps.vendors.models.certificate import Certificate
from apps.vendors.models.contact_person import ContactPerson
from django.core.mail import send_mail
from django.template.loader import render_to_string
from apps.core.utilities.generators import generate_unique_id
from apps.core.models import Address
from APP_COMPANY import APP_COMPANY


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
    organization_name = models.CharField(max_length=255, unique=True)
    alias = models.CharField(max_length=100, blank=True, null=True)
    registration_type = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    tin_number = models.CharField(max_length=255)
    vat_number = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, default="N/A")
    # address = models.ForeignKey(
    #     Address, on_delete=models.SET_NULL, null=True, blank=True
    # )
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to=upload_company_logo, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)

    active = models.BooleanField(default=False, null=True, blank=True)

    certificates = models.ManyToManyField(Certificate, related_name="vendors")
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vendors",
    )
    user_account = models.ForeignKey(
        Account,
        blank=True,
        on_delete=models.CASCADE,
        related_name="vendor_account",
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    verified = models.BooleanField(default=False, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def slug(self):
        return slugify(f"{self.organization_name}")

    def __str__(self):
        return self.organization_name

    @property
    def name(self):
        return self.organization_name

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
                "company": APP_COMPANY,
                "activated": self.active if activation is None else activation,
                "recipient": self.contact_person.full_name,  # type: ignore
            }
            html = render_to_string("vendors/activation_mail.html", context=context)
            try:
                send_mail(
                    "Account Activation",
                    "",
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    fail_silently=False,
                    recipient_list=[self.contact_person.email],  # type: ignore
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
                "organization": APP_COMPANY,
            }
            html = render_to_string("vendors/rfq_invitation_mail.html", context=context)
            try:
                send_mail(
                    "RFQ Invitation",
                    "",
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    fail_silently=False,
                    recipient_list=[self.contact_person.email],  # type: ignore
                    html_message=html,
                )
            except Exception as e:
                print("ERROR!   --->   [%s]" % e)

        thread = Thread(target=mailer)
        thread.start()
