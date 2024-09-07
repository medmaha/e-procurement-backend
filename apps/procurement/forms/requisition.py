from datetime import date
from django import forms

from ..models import (
    Requisition,
)


class RequisitionCreateForm(forms.ModelForm):
    class Meta:
        model = Requisition
        exclude = [
            "originating_officer",
            "user_department",
        ]


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        exclude = [
            "staff",
            "requisition_status",
            "requisition_number",
            "requisition_date",
        ]

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": 1, "value": 1})
    )
    estimated_unit_cost = forms.IntegerField(widget=forms.NumberInput(attrs={"min": 1}))
    estimated_total_cost = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": 1})
    )
    required_date = forms.DateField(
        widget=forms.DateInput(attrs={"min": 1, "type": "date"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for k, v in self.fields.items():
            v.widget.attrs["class"] = (
                "w-full border p-1 px-2 sm:p-2 rounded peer disabled:bg-gray-100"
            )


class RequisitionDetailForm(RequisitionForm):
    class Meta:
        model = Requisition
        fields = "__all__"

    requisition_date = forms.DateField(
        widget=forms.DateInput(attrs={"min": 1, "type": "date"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["staff"].widget.attrs["readonly"] = True
        self.fields["requisition_number"].widget.attrs["readonly"] = True
        self.fields["requisition_status"].widget.attrs["readonly"] = True
        self.fields["requisition_date"].widget.attrs["readonly"] = True
        self.fields["requisition_date"].widget.attrs["value"] = str(
            self.instance.requisition_date
        ).split(" ")[0]

    def clean_requisition_date(self):
        self.cleaned_data["requisition_date"] = (
            self.instance.requisition_date or date.today()
        )

        return self.cleaned_data["requisition_date"]

    def clean_requisition_status(self):
        self.cleaned_data["requisition_status"] = (
            self.instance.requisition_status or "pending"
        )

        return self.cleaned_data["requisition_status"]

    def clean_requisition_number(self):
        self.cleaned_data["requisition_number"] = (
            self.instance.requisition_number or "pending"
        )

        return self.cleaned_data["requisition_number"]

    def clean_total_cost(self):
        self.cleaned_data["requisition_number"] = (
            self.instance.requisition_number or "pending"
        )
        unit_cost = self.cleaned_data.get("estimated_unit_cost", 0)
        quantity = self.cleaned_data.get("quantity", 0)
        total = int(unit_cost) * int(quantity)

        self.cleaned_data["estimated_total_quantity"] = total

        return self.cleaned_data["estimated_total_quantity"]
