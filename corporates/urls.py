from django.urls import path
from . import views

urlpatterns = [
    path('<str:corp_name>/', views.corporates_search, name = 'corporates'),
    path('', views.home, name='corporate_home'),
    ]