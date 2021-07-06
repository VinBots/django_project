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
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Loading plotly Dash apps script
import django_project.dashboards.dashboard_sciencebased
import django_project.dashboards.dashboard_transparency

urlpatterns = [
    path('', views.home, name='main_home'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
	url('^dash_plot$', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
	url('^django_plotly_dash/', include('django_plotly_dash.urls')),
	path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('transparency.html', views.transparency),
    path('performance.html', views.performance),
    path('ambition.html', views.ambition),
    path('sciencebased.html', views.sciencebased),
    path('momentum.html', views.momentum),
    ]
