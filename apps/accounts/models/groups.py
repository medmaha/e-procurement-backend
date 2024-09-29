from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from apps.accounts.models.account import Account


class AuthGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    editable = models.BooleanField(blank=False, default=False)
    group_id = models.CharField(max_length=255, default="0")
    authored_by = models.CharField(max_length=255, default="system")

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Authorization Group"
        ordering = ["-last_modified", "-created_date"]

    @property
    def group(self):
        return Group.objects.filter(pk=self.group_id).first()

    def __str__(self):
        return self.name

    @classmethod
    def has_perm(cls, user: Account, code_action: str, instance=None):
        """Check if the user has the permission to create the model."""

        if not user.is_active:
            return False

        if instance:
            if instance.editable:
                return False
            if code_action == "change":
                if not instance.officer.user == user:
                    return False

        return user.has_perm(
            f"{cls._meta.app_label}.{code_action}_{cls._meta.model_name}"
        )
