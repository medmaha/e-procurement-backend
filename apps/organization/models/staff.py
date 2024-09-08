import random, uuid
from django.db import models
from apps.accounts.models import Account
from apps.organization.models.unit import Unit

from apps.core.models import Address
from apps.core.utilities.generators import generate_unique_id


class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone = models.CharField(max_length=15, unique=True)

    biography = models.TextField(blank=True, default="")

    job_title = models.CharField(
        max_length=255, default="", blank=True, help_text="The job title of the staff"
    )

    gender = models.CharField(
        max_length=25,
        default="other",
        blank=True,
        help_text="This is used to determine the permissions",
    )

    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.CASCADE
    )

    disabled = models.BooleanField(
        default=True,
        help_text="Whether staff's account is deactivated or not",
    )

    is_admin = models.BooleanField(default=False, help_text="An IT-Admin user account")

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        help_text="The unit this staff belongs to",
    )

    user_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="staff_account",
    )

    is_deleted = models.BooleanField(
        default=False, help_text="Whether staff is deleted or not"
    )
    date_deleted = models.DateTimeField(null=True, blank=True)

    DEFAULT_PASSWORD = "prc@2k2*"

    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_account)

    def __repl__(self):
        return self.__str__()

    class Meta:
        ordering = ["-created_date", "-last_modified"]

    @property
    def name(self):
        return str(self.user_account.full_name)

    @property
    def department(self):
        return self.unit.department if self.unit else None

    @property
    def permissions(self):
        return ()
