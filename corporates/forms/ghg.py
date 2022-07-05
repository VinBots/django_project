from django import forms
from corporates.models import GHGQuant
from corporates.forms.utilities import get_upload_fields_to_display


# class EntryCreationForm(forms.ModelForm):
#     class Meta:
#         model = Entry
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["corporate_name"].queryset = Corporate.objects.none()

#         if "corporate_name" in self.data:
#             self.fields["corporate_name"].queryset = Corporate.objects.all()

#         elif self.instance.pk:
#             self.fields["corporate_name"].queryset = Corporate.objects.all().filter(
#                 pk=self.instance.corporate_name.pk
#             )

REPORTING_YEAR_CHOICES = ["2020", "2021", "2022"]


class GHGForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GHGForm, self).__init__(*args, **kwargs)
        # self.fields["upload_1"].widget = forms.FileInput()
        # self.fields["upload_1"].widget.attrs = {
        #     "class": "upload_files",
        #     "id": "myclass-something",
        # }
        # self.fields["reporting_year"] = forms.DateField(
        #     widget=forms.SelectDateWidget(years=REPORTING_YEAR_CHOICES)
        # )
        self.fields_to_display = get_upload_fields_to_display(
            self.initial, upload_field_count=5
        )

    class Meta:
        model = GHGQuant
        fields = "__all__"
        localized_fields = [
            "ghg_scope_1",
            "ghg_loc_scope_2",
            "ghg_mkt_scope_2",
            "ghg_purch_scope3",
            "ghg_capital_scope3",
            "ghg_fuel_energy_loc_scope3",
            "ghg_fuel_energy_mkt_scope3",
            "ghg_upstream_td_scope3",
            "ghg_waste_ops_scope3",
            "ghg_bus_travel_scope3",
            "ghg_commute_scope3",
            "ghg_up_leased_scope3",
            "ghg_downstream_td_scope3",
            "ghg_proc_sold_scope3",
            "ghg_use_sold_scope3",
            "ghg_eol_sold_scope3",
            "ghg_down_leased_scope3",
            "ghg_franchises_scope3",
            "ghg_investments_scope3",
            "ghg_other_upstream_scope3",
            "ghg_other_downstream_scope3",
        ]
        widgets = {
            "comments": forms.Textarea(
                attrs={
                    "placeholder": "Please provide comments here",
                    "cols": 130,
                    "rows": 10,
                }
            )
        }


# GHGFormSet = forms.modelformset_factory(GHGQuant, fields="__all__", extra=1)
