# from django import forms

# from apps.procurement.models.plan import Threshold
# from apps.procurement.models.text_choices import ProcurementMethodChoice

# from ..models import Plan


# class PlanForm(forms.ModelForm):
#     class Meta:
#         model = Plan
#         fields = []

#     plan_title = forms.CharField(label="Plan Title")
#     description = forms.CharField(widget=forms.Textarea(attrs={"cols": 75}))
#     budget = forms.DecimalField(
#         label="Total Budget", decimal_places=2, widget=(forms.NumberInput())
#     )
#     threshold = forms.ChoiceField(choices=ProcurementMethodChoice.choices)

#     quarter_1_budget = forms.DecimalField(
#         decimal_places=2, widget=(forms.NumberInput())
#     )
#     quarter_2_budget = forms.DecimalField(
#         decimal_places=2, widget=(forms.NumberInput())
#     )
#     quarter_3_budget = forms.DecimalField(
#         decimal_places=2, widget=(forms.NumberInput())
#     )
#     quarter_4_budget = forms.DecimalField(
#         decimal_places=2, widget=(forms.NumberInput())
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["plan_title"].widget.attrs.update({"class": "my-custom-class"})

#     def clean_threshold(self):
#         threshold_text = self.cleaned_data["threshold"]

#         threshold = Threshold.objects.filter(procurement_method=threshold_text).first()

#         if threshold:
#             self.cleaned_data["threshold"] = threshold.pk
#             return self.cleaned_data["threshold"]

#         raise forms.ValidationError("Invalid threshold value: %s" % threshold_text)
