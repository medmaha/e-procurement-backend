from typing import Any
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.http.request import HttpRequest

# Register your models here.

from . import models


class PermissionDenied(admin.ModelAdmin):
    pass


class SupplierAdmin(PermissionDenied):
    list_display = [
        "organization_name",
        "industry",
        "contact_person",
        "license_number",
        "website",
        "tin_number",
        "established_date",
    ]

    sortable_by = []


class ContactPersonAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "full_name",
        "email",
        "phone_number",
        "address",
    ]

    sortable_by = []


class VendorRegistrationAdmin(PermissionDenied):
    list_display = [
        "vendor",
        "status",
        "last_modified",
    ]


class QuotationRespondAdmin(admin.ModelAdmin):
    readonly_fields = ["rfq", "unique_id"]
    list_display = [
        "unique_id",
        "rfq",
        "approved_status",
        "status",
        "pricing",
        "delivery_terms",
        "validity_period",
        "created_date",
    ]


admin.site.register(models.Vendor, SupplierAdmin)
admin.site.register(models.ContactPerson, ContactPersonAdmin)
admin.site.register(models.Certificate)
# admin.site.register(models.Notification)
# admin.site.register(models.QuotationItem)
admin.site.register(models.RFQResponseBrochure)
admin.site.register(models.RFQResponse, QuotationRespondAdmin)
admin.site.register(models.VendorRegistration, VendorRegistrationAdmin, index=-1)
