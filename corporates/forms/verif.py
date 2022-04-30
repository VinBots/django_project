from django import forms
from corporates.models import Verification
from corporates.forms.utilities import get_upload_fields_to_display


class VerifForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VerifForm, self).__init__(*args, **kwargs)
        self.fields_to_display = get_upload_fields_to_display(
            self.initial, upload_field_count=5
        )

    class Meta:
        model = Verification

        fields = "__all__"
        widgets = {
            "scope12_reporting_2_years": forms.RadioSelect,
            "scope12_reporting_completeness": forms.RadioSelect,
            "scope12_verification_completeness": forms.RadioSelect,
            "scope12_assurance_type": forms.RadioSelect,
            "scope3_reporting_completeness": forms.RadioSelect,
            "scope3_verification_completeness": forms.RadioSelect,
            "scope3_assurance_type": forms.RadioSelect,
        }
