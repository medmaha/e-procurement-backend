from django.db import models
from .department import Department

from apps.core.utilities.generators import generate_unique_id


class Unit(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, null=True)
    unit_head = models.ForeignKey(
        "Staff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leading_unit",
    )
    phone = models.CharField(max_length=100, default="", blank=True)
    disabled = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    enabled_since = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def unique_id(self):
        return generate_unique_id(None, self.pk)

    class Meta:
        ordering = ["-created_date", "-last_modified"]
