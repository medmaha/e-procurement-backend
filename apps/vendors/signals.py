from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.verification_db import VendorVerificationDB

from .models import VendorRegistration, Vendor, ContactPerson


@receiver(post_save, sender=ContactPerson)
def contact_person_verification(created, instance: ContactPerson, *args, **kwargs):
    if not created:
        with transaction.atomic():
            ContactPerson.objects.filter(pk=instance.pk).update(
                verified=instance.verified
            )
            Vendor.objects.filter(contact_person=instance).update(
                verified=instance.verified
            )
            VendorRegistration.objects.filter(vendor__contact_person=instance).update(
                is_validated=instance.verified
            )


@receiver(post_save, sender=Vendor)
def create_vendor_registration(created, instance: Vendor, *args, **kwargs):
    if created:
        VendorRegistration.objects.get_or_create(vendor=instance)
    else:
        VendorRegistration.objects.filter(vendor=instance).update(
            is_validated=instance.verified,
        )


@receiver(post_save, sender=VendorRegistration)
def handle_vendor_activation(created, instance, *args, **kwargs):
    if not created:
        vendor: Vendor = instance.vendor
        active = False
        changed = (instance.status == "inactive" and vendor.active) or (
            instance.status == "active" and not vendor.active
        )

        if instance.status == "active":
            active = True

        if vendor.user_account:
            if not active and changed:
                vendor.active = False
                vendor.user_account.is_active = False
                vendor.user_account.save()
                vendor.save()
                vendor.send_activation_mail(activation=False)
            elif active and changed:
                vendor.active = True
                vendor.user_account.is_active = False
                vendor.user_account.save()
                vendor.save()
                CODE = VendorVerificationDB().generate_code(vendor)
                vendor.send_activation_mail(v_code=CODE, activation=True)
