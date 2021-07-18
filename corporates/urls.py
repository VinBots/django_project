from django.urls import path
from . import views

urlpatterns = [
    path('<str:corp_name>/', views.corporates_search, name = 'corporates_search'),
    path('', views.home, name='corporates_home'),
    ]