from django import forms
from corporates.models import CDP


class CDPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CDPForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CDP
        fields = "__all__"
        # widgets = {}
