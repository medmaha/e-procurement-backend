import random, uuid
from django.db import models
from apps.accounts.models import Account
from apps.organization.models.unit import Unit

from apps.core.models import Address
from apps.core.utilities.generators import generate_unique_id


def generateEmployerNumber():
    start = int("1" + ("0" * 6))
    end = int("9" + ("0" * 6))
    suffix = str(random.randrange(start, end))
    return "EMP" + suffix


class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, default="", blank=True)
    last_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=15, default="")

    biography = models.TextField(blank=True, default="")
    job_title = models.CharField(
        max_length=255, default="", blank=True, help_text="The job title of the staff"
    )
    gender = models.CharField(
        max_length=25,
        choices=[("male", "male"), ("female", "Female"), ("other", "Other")],
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
        related_name="staffs",
        help_text="The unit this staff belongs to",
    )

    user_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        related_name="staff_account",
    )

    DEFAULT_PASSWORD = "prc@2k2*"

    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_account.full_name

    def __repl__(self):
        return "%s >> id%s " % (self.__name__, self.pk)

    class Meta:
        ordering = ["-created_date", "-last_modified"]

    @property
    def employee_id(self):
        return generate_unique_id("EM", self.pk)

    @property
    def name(self):
        return str(self.user_account.full_name)

    @property
    def user_id(self):
        return self.user_account.pk

    @property
    def department(self):
        return self.unit.department if self.unit else None

    @property
    def permissions(self):
        return ()
