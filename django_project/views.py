from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
import random
from django_project.utilities import get_top_stats, get_random_logos
from typing import Dict
import dash
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
import os
import plotly.graph_objs as go
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Group, Scheme
from django_project.dashboards.record_dashboard_benchmark import record
#from django_project.forms import EntryCreationForm
#from django_project.models import Entry, Corporates
from corporates.models import Corporate
from django.urls import reverse
from leaderboard.utilities import get_scores_xls


def home(request):

  if request.GET.get("query") is not None:
    #path = '/corporates.html/' + request.GET.get("query")
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  #form = EntryCreationForm(instance=Entry.objects.first())
  corporates_names = Corporate.objects.all()
  pct_values = get_top_stats()
  angle_deg = [str(pct_values[i] * 1.8) + "deg" for i in range(5)]


  return render (request, "django_project/home/home.html", {
    "corporates_names": corporates_names,
    "color_key_fig": "#00b118",
    "random_logos": get_random_logos(),
    "angle1":angle_deg[0],"value1":str(pct_values[0]),
    "angle2":angle_deg[1],"value2":str(pct_values[1]),
    "angle3":angle_deg[2],"value3":str(pct_values[2]),
    "angle4":angle_deg[3],"value4":str(pct_values[3]),
    "angle5":angle_deg[4], "value5":str(pct_values[4]),
    "top5_scores": get_scores_xls(corp_number=5, top_rank=True),
    "bottom5_scores": get_scores_xls(corp_number=5, top_rank=False),
    }
      )


def sectors(request, sector_name):

  sector_data = {
    "sector_name": sector_name,
    "sector_code": "xxxx"
  }
  return render (request, "django_project/sectors/main.html", sector_data)

def sectors_search(request):
  return render (request, "django_project/sectors/main.html")



