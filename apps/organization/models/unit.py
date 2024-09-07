import uuid
from django.db import models
from .department import Department

from apps.core.utilities.generators import generate_unique_id


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
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

    def save(self, *args, **kwargs):
        if self._state.adding:
            from django.utils.text import slugify
            from django.utils.crypto import get_random_string

            # capitalize company name
            self.name = " ".join(
                [name.strip().capitalize() for name in self.name.split(" ")]
            ).strip()

            # create slug
            slug_prefix = slugify(self.department.company.slug + "-")
            self.slug = slugify(slug_prefix + self.name)

            exists = Unit.objects.select_related().filter(slug=self.slug).exists()

            # create new slug if exists
            while exists:
                self.slug = slugify(
                    slug_prefix + self.name + "-" + get_random_string(5)
                )
                exists = Unit.objects.select_related().filter(slug=self.slug).exists()

        super().save(*args, **kwargs)
