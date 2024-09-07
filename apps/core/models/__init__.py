from django.db import models
from apps.accounts.models import Account


class Address(models.Model):
    country = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.to_string

    @property
    def to_string(self) -> str:
        addr = self.town
        if self.district:
            addr += " | %s" % self.district
        if self.region:
            addr += " | %s" % self.region

        addr += " | %s" % self.country
        return addr


def upload_to(instance, filename):
    path = f"vendors/id_{instance.vendor.id}/notifications/_file{instance.subject[:10]}__-{filename}"
    return path


class Notification(models.Model):
    recipient = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="owner"
    )
    message = models.TextField(max_length=255, default="")
    is_read = models.BooleanField(default=False)
    page_url = models.URLField(max_length=255, null=True)
    img_url = models.CharField(max_length=255, default="")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "%s | %s...".capitalize() % (self.recipient.last_name, self.message[:20])


class NotificationBatch(models.Model):
    is_seen = models.BooleanField(default=False, db_index=True)
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="notification_batches",
    )
    notifications = models.ManyToManyField(
        Notification, related_name="batch", related_query_name="batch"
    )
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return "Batch | %s" % (self.user.last_name)
