from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import GHGQuant
from django.urls import reverse_lazy
from django.shortcuts import render
from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):

    return render(request, "django_project/input/main.html")


class GHGList(LoginRequiredMixin, ListView):

    model = GHGQuant
    context_object_name = "ghg"
    template_name = "django_project/input/ghg/view.html"
    exclude = ["submitter", "verifier", "status"]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ghg"] = context["ghg"].filter(status="verified")
        return context


class GHGListCreate(LoginRequiredMixin, CreateView):

    model = GHGQuant
    fields = ["ghg_scope_1", "ghg_loc_scope_2", "ghg_mkt_scope_2", "ghg_purch_scope3"]
    success_url = reverse_lazy("ghg")
    template_name = "django_project/input/ghg/create.html"

    def form_valid(self, form):
        if self.submitter.username != "django":
            form.instance.submitter = self.request.user
            form.instance.verifier = ""
            form.instance.status = "submitted"
        return super(GHGListCreate, self).form_valid(form)


class GHGListUpdate(LoginRequiredMixin, UpdateView):
    model = GHGQuant
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "django_project/input/ghg/update.html"

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["ghg"] = context["ghg"].filter(status="verified")
    #     return context
