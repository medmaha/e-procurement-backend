from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.accounts.models import Account
from .models import Staff
from django.contrib.auth.models import Group


@receiver(pre_save, sender=Staff)
def staff_user_account(sender, instance: Staff, **kwargs):
    pass


@receiver(post_save, sender=Staff)
def update_staff_user_account(created, instance: Staff, **kwargs):
    pass


# @receiver(post_save, sender=Account)
# def update_user_staff_account(created, instance: Account, **kwargs):
#     if not created:
#         staff = instance.profile
#         staff.email = instance.email
#         sync_staff_account(instance, staff, )
