from typing import Any
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    pass


DEFAULT_PASSWORD = "prc@2k2*"


def upload_avatar(instance, filename: str):
    path = f"users/id_{instance.pk}/avatar/{filename}"
    return path


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to=upload_avatar,
        null=True,
        default="/img/default/avatar.png",
        blank=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    DEFAULT_PASSWORD = DEFAULT_PASSWORD
    REQUIRED_FIELDS = ["first_name", "last_name", "middle_name"]

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date", "is_active"]

    def __str__(self):
        if self.is_superuser:
            return "Superuser - @IntraSoft-ICT-SOLUTIONS"
        return self.email

    @property
    def full_name(self):
        space = " "
        if self.is_superuser:
            return self.__str__()
        return "%s%s" % (
            self.first_name,
            ((space + self.middle_name + space) if self.middle_name else space),
        ) + str(self.last_name)

    def save(self, *args, **kwargs):
        if not self.password:  # type: ignore
            raise ValueError("The Password field must be set")
        return super().save(*args, **kwargs)

    @property
    def profile(self):
        _, profile = self.get_profile()
        return profile

    @property
    def profile_type(self):
        name, _ = self.get_profile()

        if name:
            return name
        return "Admin"

    def get_profile(self) -> tuple[str, Any]:
        staff = self.staff_account.filter().first()  # type: ignore
        if staff:  # type: ignore
            return ("Staff", staff)
        vendor = self.vendor_account.filter().first()  # type: ignore
        if vendor:
            return ("Vendor", vendor)
        gppa = self.gppa_account.filter().first()  # type: ignore
        if gppa:
            return ("GPPA", gppa)
        if self.is_superuser:
            return ("Admin", None)
        return ("None", None)

    def __groups__(self):
        return self.groups.all().count()
