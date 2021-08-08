from django.shortcuts import render
import os
from leaderboard.utilities import get_scores_xls

# Create your views here.


def leaderboard_home(request):
    
    return render(
        request,
        "django_project/leaderboard/main.html",
        {'scores':get_scores_xls()}
        )
