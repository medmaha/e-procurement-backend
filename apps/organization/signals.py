from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.accounts.models import Account
from .models import Staff
from django.contrib.auth.models import Group


@receiver(pre_save, sender=Staff)
def staff_user_account(sender, instance: Staff, **kwargs):
    from apps.core.constants import DefaultGroups

    if not instance.user_account_id:  # type: ignore
        account = Account(
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
            middle_name=instance.middle_name,
            is_active=not instance.disabled or instance.is_admin,
            is_staff=instance.is_admin,
            is_superuser=False,
        )
        if account.is_active:
            instance.disabled = False
        account.set_password(account.DEFAULT_PASSWORD)
        account.save()

        staff_group, _ = Group.objects.get_or_create(
            name=DefaultGroups.STAFF_MEMBER["name"]
        )
        account.groups.add(staff_group)

        instance.user_account = account  # type: ignore


@receiver(post_save, sender=Staff)
def update_staff_user_account(created, instance: Staff, **kwargs):
    if not created:
        account_queryset = Account.objects.filter(pk=instance.user_account.pk)
        account_queryset.update(
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
            middle_name=instance.middle_name,
            is_active=not instance.disabled,
            is_staff=instance.is_admin,
        )


# @receiver(post_save, sender=Account)
# def update_user_staff_account(created, instance: Account, **kwargs):
#     if not created:
#         staff = instance.profile
#         staff.email = instance.email
#         sync_staff_account(instance, staff, )
