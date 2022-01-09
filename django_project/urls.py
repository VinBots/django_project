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
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),	
    path('', views.home, name='main_home'),
    path('corporates.html/', include('corporates.urls')),
    #path('sectors.html/<str:sector_name>/', views.sectors, name = 'sectors'),
    #path('sectors.html/', views.sectors_search, name = 'sectors_search'),
    path('aboutus.html/', views.aboutus, name = 'aboutus'),
    path('faq.html/', views.faq, name = 'faq'),
    path('blog.html/', views.blog, name = 'blog'),
    path('leaderboard.html/', include('leaderboard.urls')),
    path('download/', views.download_file, name = 'download_file'),
    path('download/<str:folder_name>/<str:file_name>', views.download_file, name = 'download_file'),
    path('market.html/', include('market.urls')),
    ]