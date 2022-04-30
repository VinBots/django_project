from django.views import View
from django.shortcuts import render

from corporates.views.input.permissions import AllowedCorporateMixin
from corporates.models import Corporate


class InputComments(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "comments"
        kwargs["company_id"] = Corporate.objects.filter(name=kwargs["corp_name"])[
            0
        ].company_id

        return render(request, self.template_name, *args, kwargs)
