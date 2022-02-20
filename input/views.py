from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import GHGQuant
from django.urls import reverse_lazy


class GHGList(ListView):

    model = GHGQuant
    context_object_name = "ghg"
    template_name = "input/ghg/view.html"


class GHGListCreate(CreateView):

    model = GHGQuant
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "input/ghg/create.html"


class GHGListUpdate(UpdateView):
    model = GHGQuant
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "input/ghg/update.html"
