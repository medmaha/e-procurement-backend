from email.policy import default
from django.db import models
from apps.vendors.models import Vendor


class VendorRegistration(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True)
    status = models.CharField(
        max_length=255,
        choices=(
            (
                "inactive",
                "Inactive",
            ),
            ("active", "Active"),
        ),
        default="inactive",
    )
    is_validated = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vendor Registration"
        verbose_name_plural = "Vendor Registration"
        ordering = ["-created_date", "-last_modified", "status"]
