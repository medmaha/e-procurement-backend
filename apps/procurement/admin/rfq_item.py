from django.contrib import admin

from apps.procurement import forms
from ..models import RFQItem

from django import forms


class Form(forms.ModelForm):
    class Meta:
        model = RFQItem
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "measurement_unit" in self.fields:
            self.fields["measurement_unit"].label = "M-Unit"


class RFQItemAdmin(admin.TabularInline):
    model = RFQItem
    form = Form
    extra = 0
