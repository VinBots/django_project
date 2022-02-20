from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import GHGQuant
from django.urls import reverse_lazy
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):

    return render(request, "django_project/input/main.html")


class GHGList(LoginRequiredMixin, ListView):

    model = GHGQuant
    context_object_name = "ghg"
    template_name = "django_project/input/ghg/view.html"


class GHGListCreate(LoginRequiredMixin, CreateView):

    model = GHGQuant
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "django_project/input/ghg/create.html"


class GHGListUpdate(LoginRequiredMixin, UpdateView):
    model = GHGQuant
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "django_project/input/ghg/update.html"
