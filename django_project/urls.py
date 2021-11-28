"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.shortcuts import render
from django.contrib import admin
#from django.conf.urls import url
from django.urls import path, include
from . import views
#from django.views.generic import TemplateView
#from django.conf import settings
#from django.conf.urls.static import static
#from typing import Dict
#import dash
#import dash_table
#from dash.dependencies import Input, Output
#import pandas as pd
#from django_plotly_dash import DjangoDash
#import dash_html_components as html
#from django_project.utilities import get_data
#import dash_core_components as dcc
#import os
#import plotly.graph_objs as go
#import dash_table.FormatTemplate as FormatTemplate
#from dash_table.Format import Format, Group, Scheme


# Loading plotly Dash apps script
#dashboards_names = [
    #"django_project.dashboards.dashboard_transparency",
    #"django_project.dashboards.dashboard_performance",
    #"django_project.dashboards.dashboard_ambition",
    #"django_project.dashboards.dashboard_sciencebased",
    #"django_project.dashboards.dashboard_momentum",
    #"django_project.dashboards.dashboard_playground",
    #"django_project.dashboards.dashboard_benchmark"
    #]

#for lib in dashboards_names:
    #globals()[lib] = __import__(lib)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),	
    path('', views.home, name='main_home'),
    path('corporates.html/', include('corporates.urls')),
    path('sectors.html/<str:sector_name>/', views.sectors, name = 'sectors'),
    path('sectors.html/', views.sectors_search, name = 'sectors_search'),
    path('aboutus.html/', views.aboutus, name = 'aboutus'),
    path('faq.html/', views.faq, name = 'faq'),
    path('blog.html/', views.blog, name = 'blog'),
    path('leaderboard.html/', include('leaderboard.urls')),
    path('download/', views.download_file, name = 'download_file'),
    ]

    #OLD paths
    #url('^dash_plot$', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
	#url('^django_plotly_dash/', include('django_plotly_dash.urls')),
	#path('home', TemplateView.as_view(template_name='home.html'), name='home'),