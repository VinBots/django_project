from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from corporates.models import UserProfile, Corporate


class ChooseCorporateList(LoginRequiredMixin, ListView):

    model = UserProfile
    template_name = "django_project/input/main.html"
    context_object_name = "data"

    def dispatch(self, request, *args, **kwargs):

        if self.request.GET.get("corp") is not None:
            path = reverse(
                "input_by_corp_general",
                kwargs={"corp_name": self.request.GET.get("corp")},
            )
            print("NOT GET QUERY")
            return redirect(path)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if not self.is_allowed_corporates_all():
            corp_list_query = (
                super()
                .get_queryset()
                .filter(user=self.request.user)
                .values_list("allowed_corporates__name")
            )
            return [corp[0] for corp in corp_list_query]
        else:
            return Corporate.objects.all()

    def is_allowed_corporates_all(self):

        test1 = UserProfile.objects.filter(
            user=self.request.user, allowed_corporates_all=True
        ).exists()
        return test1
