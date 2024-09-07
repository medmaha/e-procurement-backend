import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Company(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)

    contact_email = models.EmailField(unique=True, db_index=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)

    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    coordinates = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(
        max_length=50, blank=True, default="The Gambia", db_index=True
    )

    website_url = models.URLField(null=True, blank=True)
    industry = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    tax_id = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    license_number = models.CharField(max_length=20, null=True, blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    registration_certificate_url = models.URLField(null=True, blank=True)

    verified = models.BooleanField(default=False, blank=True)
    date_verified = models.DateTimeField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, db_index=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-last_modified", "-created_date"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:

            # capitalize company name
            self.name = " ".join(
                [name.strip().capitalize() for name in self.name.split(" ")]
            ).strip()

            # create slug
            self.slug = slugify(self.name)

            exists = Company.objects.select_related().filter(slug=self.slug).exists()

            # create new slug if exists
            while exists:
                self.slug = slugify(self.name + "-" + get_random_string(5))
                exists = (
                    Company.objects.select_related().filter(slug=self.slug).exists()
                )

        super().save(*args, **kwargs)
