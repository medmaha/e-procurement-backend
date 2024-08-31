from django import forms
from .. import models


class DepartmentRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Department
        exclude = []
