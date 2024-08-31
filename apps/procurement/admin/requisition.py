from django.contrib import admin
from ..models import Requisition
from django import forms


class Form(forms.ModelForm):
    class Meta:
        model = Requisition
        exclude = []


class RequisitionAdmin(admin.ModelAdmin):
    model = Requisition
    form = Form
