from django import forms
from corporates.models import Entry, Corporate


class EntryCreationForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['corporate_name'].queryset = Corporate.objects.none()

        if 'corporate_name' in self.data:
            self.fields['corporate_name'].queryset = Corporate.objects.all()

        elif self.instance.pk:
            self.fields['corporate_name'].queryset = Corporate.objects.all().filter(pk=self.instance.corporate_name.pk)