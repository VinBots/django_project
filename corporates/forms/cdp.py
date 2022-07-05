from django import forms
from corporates.models import CDP


class CDPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CDPForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CDP
        fields = "__all__"
        widgets = {
            "made_public": forms.RadioSelect,
            "comments": forms.Textarea(
                attrs={
                    "placeholder": "Please provide any comment about the CDP Climate Change Questionnaire here",
                    "cols": 130,
                    "rows": 10,
                }
            ),
        }
