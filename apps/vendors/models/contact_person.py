from django.db import models

from apps.core.models import Address


class ContactPerson(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"  # type: ignore

    class Meta:
        verbose_name = "Contact Person"
        ordering = ["-created_date", "-last_modified", "verified"]

    @property
    def organization(self):
        if self.vendor:
            return f"{self.vendor.name}"  # type: ignore

    @property
    def full_name(self) -> str:
        return str(self)

    @property
    def vendor(self):
        return self.vendors.first()  # type: ignore
