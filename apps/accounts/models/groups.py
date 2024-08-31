from django.db import models
from django.contrib.auth.models import Group


class AuthGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    editable = models.BooleanField(blank=False, default=False)
    group_id = models.CharField(max_length=255, default="0")
    authored_by = models.CharField(max_length=255, default="system")

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Group"
        ordering = ["-last_modified", "-created_date"]

    @property
    def group(self):
        return Group.objects.filter(pk=self.group_id).first()

    def __str__(self):
        return self.name
