from django import forms
from .. import models


class UnitRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Department
        exclude = ["unit_head"]
