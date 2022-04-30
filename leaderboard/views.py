from django.shortcuts import render
from leaderboard.utilities import get_scores_db


def leaderboard_home(request):

    return render(
        request,
        "django_project/leaderboard/main.html",
        {
            "scores_db": get_scores_db(),
        },
    )
