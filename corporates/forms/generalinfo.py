from django import forms
from corporates.models import GeneralInfo


class GeneralInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GeneralInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GeneralInfo
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Please provide a short description of the document here",
                    "cols": 130,
                    "rows": 10,
                }
            ),
        }
