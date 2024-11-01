from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.organization.models import Staff


class Delegation(models.Model):
    """
    Model to handle temporary delegation of approval authority.
    """

    delegator = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="delegated_from"
    )
    delegate = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="delegated_to"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)

    def clean(self):
        """
        Validate delegation dates.
        """
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < timezone.now():
            raise ValidationError("Start date cannot be in the past")

    def save(self, *args, **kwargs):
        """
        Perform validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.delegator} delegated to {self.delegate} ({self.start_date} to {self.end_date})"
