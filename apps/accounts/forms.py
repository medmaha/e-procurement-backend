from django import forms
from apps.accounts.models import Account
from apps.vendors.models import Vendor


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = [
            "user_permissions",
            "is_superuser",
            "is_staff",
            "unique_id",
            "password",
        ]


class VendorCreateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ["director", "user"]


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
