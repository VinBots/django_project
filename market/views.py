from django.shortcuts import render
import os
from market.utilities import get_market_stats

# Create your views here.


def market_home(request):
    
    return render(
        request,
        "django_project/market/main.html",
        {'market_stats':get_market_stats()}
        )
