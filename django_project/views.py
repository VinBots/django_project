from corporates.models import Corporate
from django.urls import reverse
from leaderboard.utilities import get_scores_xls
from django.shortcuts import render, redirect
from django_project.utilities import get_random_logos, get_top10_wo_zero, get_top5_transp_miss_cut
import mimetypes
import os
from django.http import HttpResponse
from pathlib import Path


#import random
#from typing import Dict
#import dash
#import dash_table
#from dash.dependencies import Input, Output
#import pandas as pd
#from django_plotly_dash import DjangoDash
#import dash_html_components as html
#import dash_core_components as dcc
#import plotly.graph_objs as go
#import dash_table.FormatTemplate as FormatTemplate
#from dash_table.Format import Format, Group, Scheme
#from django_project.dashboards.record_dashboard_benchmark import record
#from django_project.forms import EntryCreationForm
#from django_project.models import Entry, Corporates


def home(request):

  if request.GET.get("query") is not None:
    #path = '/corporates.html/' + request.GET.get("query")
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  #form = EntryCreationForm(instance=Entry.objects.first())
  corporates_names = Corporate.objects.all()
  pct_values = [16, 50, 42]  #get_top_stats()
  angle_deg = [str(pct_values[i] * 1.8) + "deg" for i in range(3)]


  return render (request, "django_project/home/main.html", {
    "corporates_names": corporates_names,
    #"color_key_fig": "#00b118",
    "random_logos": get_random_logos(),
    "angle1":angle_deg[0],"value1":str(pct_values[0]),
    "angle2":angle_deg[1],"value2":str(pct_values[1]),
    "angle3":angle_deg[2],"value3":str(pct_values[2]),
    # "angle4":angle_deg[3],"value4":str(pct_values[3]),
    # "angle5":angle_deg[4], "value5":str(pct_values[4]),
    "top5_scores": get_scores_xls(corp_number=5, top_rank=True),
    "bottom5_scores": get_scores_xls(corp_number=5, top_rank=False),
    "top10_wo_zero" : get_top10_wo_zero()
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

def aboutus(request):
  return render (request, "django_project/aboutus/main.html")

def blog(request):

  return render (
    request,
    "django_project/blog/main.html",
    {
      "top5_mising_cut": get_top5_transp_miss_cut(),
    }
  )

def faq(request):
  return render (request, "django_project/faq/main.html")


def download_file (request, filename = ''):#filename = '2020_43_1.pdf'):

    if filename !='':
      BASE_DIR_LIB = os.path.join(Path(__file__).parent.parent.parent,'net0_docs','reports')
      filepath = os.path.join (BASE_DIR_LIB, 'ghg', filename)
      path = open(filepath, 'r')
      # Set the mime type
      mime_type, _ = mimetypes.guess_type(filepath)
      # Set the return value of the HttpResponse
      response = HttpResponse(path, content_type=mime_type)
      # Set the HTTP header for sending to browser
      response['Content-Disposition'] = "attachment; filename=%s" % filename
      # Return the response value
      return response