from django.db import models
from django.forms import CharField


def upload_company_certificates(instance, filename: str):
    path = f"vendors/id_{instance.vendor.id}/certificates/{filename}"
    return path


class Certificate(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    achieved_from = models.CharField(max_length=100)
    date_achieved = models.DateField(auto_now_add=True)
    vendor = models.ForeignKey(
        "Vendor",
        on_delete=models.CASCADE,
        null=True,
        related_name="certificate_sets",
        blank=True,
    )
    verified = models.BooleanField(default=False)
    file = models.FileField(upload_to=upload_company_certificates, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date", "name"]

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs):
        # TODO: delete all files associated with this company
        return super().delete(*args, **kwargs)

    @property
    def organization_name(self):
        return str(self.vendor)  # type: ignore
