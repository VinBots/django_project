import re
from corporates.models import Corporate
from django.urls import reverse
from leaderboard.utilities import get_scores_xls
from django.shortcuts import render, redirect
from django_project.utilities import (
    get_random_logos,
    get_top10_wo_zero,
    get_top5_transp_miss_cut,
)
import os
from django.http import HttpResponse
from django.core.files import File
from django_project.utilities import get_general_stats

# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from config import Config as c


def home(request):

    if request.GET.get("query") is not None:
        path = reverse("corporates_home") + request.GET.get("query")
        return redirect(path)

    corporates_names = Corporate.objects.all()

    return render(
        request,
        "django_project/home/main.html",
        {
            "corporates_names": corporates_names,
            "random_logos": get_random_logos(),
            "general_stats": get_general_stats(["trust", "commitments", "science"]),
            "top5_scores": get_scores_xls(corp_number=5, top_rank=True),
            "bottom5_scores": get_scores_xls(corp_number=5, top_rank=False),
            "top10_wo_zero": get_top10_wo_zero(),
        },
    )


def aboutus(request):
    return render(request, "django_project/aboutus/main.html")


def blog(request):

    return render(
        request,
        "django_project/blog/main.html",
        {
            "top5_mising_cut": get_top5_transp_miss_cut(),
        },
    )


def faq(request):
    return render(request, "django_project/faq/main.html")


def download_file(request, folder_name="", file_name=""):

    if file_name != "":
        BASE_DIR_LIB = os.path.join(c.DATA_FOLDER, c.LIBRARY_FOLDER)
        filepath = os.path.join(BASE_DIR_LIB, folder_name, file_name)
        if os.path.exists(filepath):
            f = open(filepath, "rb")
            pdfFile = File(f)
            response = HttpResponse(pdfFile.read())
            response["Content-Disposition"] = "attachment;filename=%s" % file_name
            return response
        else:
            return None
    else:
        return redirect(reverse("main_home"))


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account as created for " + user)
            return redirect("loginpage")
    context = {"form": form}
    return render(request, "django_project/accounts/register.html", context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main_home")
        else:
            messages.info(request, "Username OR password is incorrect")

    context = {}
    return render(request, "django_project/accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("loginpage")
