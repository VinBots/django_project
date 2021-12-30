from django.shortcuts import render
import os
from leaderboard.utilities import get_scores_xls

# Create your views here.


def market_home(request):
    
    return render(
        request,
        "django_project/market/main.html",
        {'scores':get_scores_xls()}
        )
