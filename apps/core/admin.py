from django.contrib import admin
from . import models

admin.site.register(models.Address)
admin.site.register(models.Notification)
admin.site.register(models.NotificationBatch)
