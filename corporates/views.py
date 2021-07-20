from django.shortcuts import render, redirect
from corporates.models import Corporate
from django.urls import reverse
from corporates.utilities import get_path_to_bubble, check_validity, get_ghg_xls



def corporates_search(request, corp_name=None):

  if request.GET.get("query") is not None:
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  if check_validity(corp_name):
    selected_corp = Corporate.objects.get(name=corp_name)
    xls_corp = {
      'ghg': get_ghg_xls(corp_name)
    }

    corp_data = {
    "selected_corp": selected_corp,
    "xls_corp": xls_corp,
    "selected_corp_bubble_chart": get_path_to_bubble(selected_corp.filename),
    }
    
    return render (request, "django_project/corporates/main.html", corp_data)
  else:
    return render(
      request, 
      "django_project/corporates/home.html", 
      {"error_msg":"No match found",
      "corporates_names": Corporate.objects.all(),
      }
      )


def corporates_home(request):

  if request.GET.get("query") is not None:
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  return render(
    request,
    "django_project/corporates/home.html", 
    {
      "error_msg":"",
      "corporates_names": Corporate.objects.all()
    }
    )