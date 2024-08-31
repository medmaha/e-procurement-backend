from datetime import date
from django import forms

from apps.organization.models import Staff
from apps.core.utilities.text_choices import (
    ApprovalChoices,
)

from ..models import (
    RFQ,
)


class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = []

    rfq_date = forms.DateField(
        widget=forms.DateInput(attrs={"readonly": True, "value": date.today})
    )
    originating_officer = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": True}),
        label="Employee ID",
        help_text="This is your employee ID",
    )
    officer_department = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": True}),
        label="Employee Department",
        help_text="This is your current department",
    )
    requisition_number = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        help_text="The requisition number for this request for quotation",
    )
    required_date = forms.DateField(
        label="Latest submission date",
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="After the specified date, The RFQ will automatically expire. Unless you update the date",
    )

    notes_for_vendors = forms.CharField(
        label="Notes for Vendors",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 75}),
        required=False,
    )
    label_for_vendors_to_complete = forms.CharField(
        label="Label for Vendors to Complete",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 75}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_value in self.fields.values():
            field_value.widget.attrs.update(
                {
                    "class": "mt-1 p-2 border border-gray-300 rounded w-full opacity-80 bg-gray-50 invalid:border-red-500 focus:text-current disabled:opacity-40 disabled:bg-white"
                }
            )


class RFQEditForm(RFQForm):
    approval_status = forms.ChoiceField(
        widget=forms.Select(), choices=ApprovalChoices.choices
    )
    approval_officer = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Staff.objects.filter(),
        required=False,
    )
    officer_department = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": True}),
        label="Employee Department",
        help_text="This is your current department",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
