import re
from typing import Any
from django import forms

from apps.core.utilities.text_choices import MeasurementUnitChoices

from ..models import RFQItem


class RFQItemsForm(forms.ModelForm):
    # Customizing labels and widgets if needed
    class Meta:
        model = RFQItem
        fields = []

    item_description = forms.CharField(
        label="Item Description",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter product or service description"}
        ),
    )
    quantity = forms.IntegerField(label="QTY", min_value=1)
    measurement_unit = forms.ChoiceField(choices=MeasurementUnitChoices.choices)
    unit_price = forms.IntegerField(label="Unit Price", min_value=0)
    evaluation_criteria = forms.CharField(
        label="Eva Criteria", widget=forms.TextInput(attrs={"rows": 2}), required=False
    )
    comment = forms.CharField(
        label="Remark", widget=forms.TextInput(attrs={}), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_value in self.fields.values():
            field_value.widget.attrs.update(
                {
                    "class": "mt-1 p-2 border border-gray-300 rounded w-full opacity-80 bg-gray-50 invalid:border-red-500 focus:text-current disabled:opacity-40 disabled:bg-white"
                }
            )

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity is not None and quantity >= 1:
            self.cleaned_data["quantity"] = quantity
            return quantity
        raise forms.ValidationError("Invalid quantity value ")

    def clean_unit_price(self):
        unit_price = self.cleaned_data["unit_price"]
        if unit_price is not None and unit_price >= 0:
            self.cleaned_data["unit_price"] = unit_price
            return unit_price
        raise forms.ValidationError("Invalid amount specified for unit price")


class RFQItemEditForm(RFQItemsForm):
    measurement_unit = forms.ChoiceField(
        choices=MeasurementUnitChoices.choices, label="M-Unit"
    )
    total_price = forms.DecimalField(
        label="Total Cost",
        required=False,
        widget=forms.NumberInput(attrs={"readonly": True}),
    )
    comment = forms.CharField(
        label="Remark", widget=forms.TextInput(attrs={"rows": 2}), required=False
    )
