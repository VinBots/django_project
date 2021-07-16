from django import forms
from django_project.models import Entry, Corporates


class EntryCreationForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['corporate_name'].queryset = Corporates.objects.none()

        if 'corporate_name' in self.data:
            self.fields['corporate_name'].queryset = Corporates.objects.all()

        elif self.instance.pk:
            self.fields['corporate_name'].queryset = Corporates.objects.all().filter(pk=self.instance.corporate_name.pk)