from django.conf import UserSettingsHolder
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from corporates.forms import GHGForm
from models import GHGQuant, UserProfile
from django.urls import reverse_lazy
from django.shortcuts import render

from django.shortcuts import render, redirect
from corporates.models import Corporate
from django.urls import reverse
from corporates.utilities import (
    AllowedCorporateMixin,
    get_company_id_from_name,
)


def home(request):

    return render(request, "django_project/input/main.html")


def input_home(request):

    return render(request, "django_project/input/main.html")


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


class InputGeneral(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "general"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


class GHGListCreate(AllowedCorporateMixin, CreateView):

    initial = {}
    form_class = GHGForm
    template_name = "django_project/input/corp_ghg.html"

    def get(self, request, *args, **kwargs):

        form = self.form_class(initial=self.initial)
        kwargs["form"] = form
        kwargs["category"] = "ghg"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = reverse(
            "input_by_corp_general", kwargs={"corp_name": context["corp_name"]}
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        if self.request.user != "django":
            form.instance.submitter = self.request.user
            # form.instance.verifier = "pending"
            form.instance.status = "submitted"
        return super(GHGListCreate, self).form_valid(form)


class GHGListUpdate(AllowedCorporateMixin, UpdateView):

    initial = {}
    form_class = GHGForm
    template_name = "django_project/input/corp_ghg.html"

    def get(self, request, *args, **kwargs):

        form = self.form_class(initial=self.initial)
        kwargs["form"] = form
        kwargs["category"] = "ghg"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = reverse(
            "input_by_corp_general", kwargs={"corp_name": context["corp_name"]}
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        if self.request.user != "django":
            form.instance.submitter = self.request.user
            # form.instance.verifier = "pending"
            form.instance.status = "submitted"
        return super(GHGListCreate, self).form_valid(form)


class InputVerification(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "verification"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


class InputTargets(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "targets"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


class InputComments(AllowedCorporateMixin, View):

    template_name = "django_project/input/corp_general.html"

    def get(self, request, *args, **kwargs):
        kwargs["category"] = "comments"
        kwargs["company_id"] = get_company_id_from_name(kwargs["corp_name"])

        return render(request, self.template_name, *args, kwargs)


# class GHGListUpdate(AllowedCorporateMixin, UpdateView):
#     model = GHGQuant
#     fields = "__all__"
#     success_url = reverse_lazy("ghg")
#     template_name = "django_project/input/ghg/update.html"

#     # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#     #     context = super().get_context_data(**kwargs)
#     #     context["ghg"] = context["ghg"].filter(status="verified")
#     #     return context
