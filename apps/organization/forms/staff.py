from django import forms
from .. import models


class StaffsRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Department
        exclude = ["unit"]
