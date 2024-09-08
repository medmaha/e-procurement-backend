import uuid
from django.db import models
from django.contrib.auth.models import Group, Permission


class AuthGroup(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    group_id = models.CharField(max_length=255, default="0")
    editable = models.BooleanField(blank=False, default=False)
    authored_by = models.CharField(max_length=255, default="system")

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Group"
        ordering = ["-last_modified", "-created_date"]

    @property
    def group(self):
        return Group.objects.filter(pk=self.group_id).first()

    @property
    def permissions(self):
        return Permission.objects.filter(group=self.group)

    def __str__(self):
        return self.name
