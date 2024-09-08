from typing import Any
import uuid
from django.db import models
from django.contrib.auth.models import (
    UserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class AccountManager(UserManager):

    def create_superuser(self, email: str, password: str, **kwargs: Any):
        account = Account(email=email, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.is_active = True
        account.set_password(password)
        account.full_clean()
        account.save(using=self._db)

        return account


DEFAULT_PASSWORD = "prc@2k2*"


def upload_avatar(instance, filename: str):
    path = f"users/id_{instance.pk}/avatar/{filename}"
    return path


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    avatar = models.CharField(
        default="/img/default/avatar.png",
        null=True,
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

    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date", "is_active"]

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not ("sha256" in self.password):
                self.set_password(self.password or self.DEFAULT_PASSWORD)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        space = " "
        return "%s%s" % (
            self.first_name,
            ((space + self.middle_name + space) if self.middle_name else space),
        ) + str(self.last_name)

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
        staff = self.staff_account.first()  # type: ignore
        if staff:  # type: ignore
            return ("Staff", staff)
        vendor = self.vendor_account.first()  # type: ignore
        if vendor:
            return ("Vendor", vendor)
        gppa = self.gppa_account.first()  # type: ignore
        if gppa:
            return ("GPPA", gppa)
        if self.is_staff:
            # TODO: return a System admin Profile
            return ("Admin", None)
        return ("None", None)

    def __groups__(self):
        return self.groups.all().count()
