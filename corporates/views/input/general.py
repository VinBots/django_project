from django.views import View
from django.shortcuts import render

from corporates.models import Corporate

from corporates.views.input.permissions import AllowedCorporateMixin


class InputGeneral(AllowedCorporateMixin, View):
    """
    Handles the 'General' section of the input interface
    """

    template_name = "django_project/input/general/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "general"
        kwargs["company_id"] = Corporate.objects.filter(name=kwargs["corp_name"])[
            0
        ].company_id

        return render(request, self.template_name, *args, kwargs)
