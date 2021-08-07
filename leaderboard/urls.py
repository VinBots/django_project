from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard_home, name='leaderboard_home'),
    ]