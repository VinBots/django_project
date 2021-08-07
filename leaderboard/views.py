from django.shortcuts import render
import os
from leaderboard.utilities import get_scores_xls

# Create your views here.


def leaderboard_home(request):
    
    scores_dict = get_scores_xls()

    return render(
        request,
        "django_project/leaderboard/main.html",
        {'scores':scores_dict}
        )
