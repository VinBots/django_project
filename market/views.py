from django.shortcuts import render

from market.utilities import get_market_stats, get_meta_data


def market_home(request):

    return render(
        request,
        "django_project/market/main.html",
        {"market_stats": get_market_stats(), "meta": get_meta_data()},
    )
