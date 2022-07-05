from django import forms
from corporates.models import TargetQuant
from corporates.forms.utilities import get_upload_fields_to_display


class TargetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TargetForm, self).__init__(*args, **kwargs)
        self.fields_to_display = get_upload_fields_to_display(
            self.initial, upload_field_count=5
        )

    class Meta:
        model = TargetQuant
        fields = "__all__"
        widgets = {
            "type": forms.RadioSelect,
            "source": forms.RadioSelect,
            "sbti_status": forms.RadioSelect,
            "scope_coverage": forms.RadioSelect,
            "scope_3_coverage": forms.RadioSelect,
            "net0_valid": forms.RadioSelect,
            "scope": forms.RadioSelect,
            "cov_s1": forms.RadioSelect,
            "cov_s2_mkt": forms.RadioSelect,
            "cov_s2_loc": forms.RadioSelect,
            "cov_s3": forms.RadioSelect,
            "comments": forms.Textarea(
                attrs={
                    "placeholder": "Please provide comments here",
                    "cols": 130,
                    "rows": 10,
                }
            ),
        }
