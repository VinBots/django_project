from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import GHGQuantPublic


from django.shortcuts import render, redirect
from corporates.models import Corporate, GHGQuantPublic
from django.urls import reverse, reverse_lazy
from corporates.utilities import (
    get_library_data,
    get_path_to_chart,
    check_validity,
    get_ghg,
    get_path_to_img,
    get_score_data,
    get_scores_summary,
    get_targets,
    file_exist,
    get_scores_details,
    get_all_data_from_csv,
)
from django_project.utilities import get_random_logos
from pathlib import Path
import os
from config import Config as c


class GHGList(ListView):

    model = GHGQuantPublic
    context_object_name = "ghg"
    template_name = "input/ghg/view.html"


class GHGListCreate(CreateView):

    model = GHGQuantPublic
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "input/ghg/create.html"


class GHGListUpdate(UpdateView):
    model = GHGQuantPublic
    fields = "__all__"
    success_url = reverse_lazy("ghg")
    template_name = "input/ghg/update.html"
