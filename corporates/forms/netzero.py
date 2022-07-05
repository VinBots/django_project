from django import forms
from corporates.models import NetZero
from corporates.forms.utilities import get_upload_fields_to_display


class NetZeroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NetZeroForm, self).__init__(*args, **kwargs)
        self.fields_to_display = get_upload_fields_to_display(
            self.initial, upload_field_count=5
        )

    class Meta:
        model = NetZero
        fields = "__all__"
        widgets = {
            "stated": forms.RadioSelect,
            "coverage": forms.RadioSelect,
            "already_reached": forms.RadioSelect,
            "ongoing_coverage": forms.RadioSelect,
            "ongoing": forms.RadioSelect,
            "ongoing_scope_3_coverage": forms.RadioSelect,
            "scope_3_coverage": forms.RadioSelect,
            "comments": forms.Textarea(
                attrs={
                    "placeholder": "Please provide comments here",
                    "cols": 130,
                    "rows": 10,
                }
            ),
        }
