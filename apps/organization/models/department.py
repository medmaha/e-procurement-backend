import uuid
from django.db import models

from apps.app.models.company import Company


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    department_head = models.ForeignKey(
        "Staff", on_delete=models.SET_NULL, null=True, blank=True
    )
    phone = models.CharField(max_length=100, default="", blank=True)
    disabled = models.BooleanField(default=False)

    last_modified = models.DateTimeField(auto_now=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    enabled_since = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            from django.utils.text import slugify
            from django.utils.crypto import get_random_string

            # capitalize company name
            self.name = " ".join(
                [name.strip().capitalize() for name in self.name.split(" ")]
            ).strip()

            # create slug
            slug_prefix = slugify(self.company.slug + "-")
            self.slug = slugify(slug_prefix + self.name)

            exists = Department.objects.select_related().filter(slug=self.slug).exists()

            # create new slug if exists
            while exists:
                self.slug = slugify(
                    slug_prefix + self.name + "-" + get_random_string(5)
                )
                exists = (
                    Department.objects.select_related().filter(slug=self.slug).exists()
                )

        super().save(*args, **kwargs)
