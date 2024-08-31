from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)
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
