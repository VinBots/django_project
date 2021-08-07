from django.shortcuts import render
import os


# Create your views here.


def leaderboard_home(request):
    
    data_dict = {}

    return render(
        request,
        "django_project/leaderboard/main.html",
        data_dict
        )
