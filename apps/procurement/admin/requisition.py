from django.contrib import admin
from ..models import Requisition
from django import forms


class Form(forms.ModelForm):
    class Meta:
        model = Requisition
        exclude = []


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    form = Form
