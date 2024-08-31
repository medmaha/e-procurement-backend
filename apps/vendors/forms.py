from django import forms
from . import models


class CertificateCreateForm(forms.ModelForm):
    class Meta:
        model = models.Certificate
        fields = "__all__"


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = models.ContactPerson
        fields = "__all__"


class VendorCreateForm(forms.ModelForm):
    class Meta:
        model = models.Vendor
        fields = "__all__"


class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Vendor
        fields = ["logo"]


class QuoteForm(forms.ModelForm):
    class Meta:
        model = models.RFQResponse
        fields = [
            "remarks",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remarks"].label = "Comment or Remark"
        self.fields["remarks"].widget.attrs["rows"] = "3"
        for field in self.fields.values():
            field.widget.attrs[
                "class"
            ] = "w-full border p-1.5 px-2 rounded peer disabled:bg-white mb-4"
