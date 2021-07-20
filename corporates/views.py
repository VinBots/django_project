from django.shortcuts import render, redirect
from corporates.models import Corporate
from django.urls import reverse
from corporates.parameters import get_path_to_bubble

# Create your views here.

def corporates_search(request, corp_name=None):

  if request.GET.get("query") is not None:
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  if check_validity(corp_name):
    selected_corp = Corporate.objects.get(name=corp_name)
    
    corp_data = {
    "selected_corp": selected_corp,
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


def check_validity(corp_name):

  cond1 = corp_name is not None
  #corporates_names = Corporate.objects.all()
  cond2 = Corporate.objects.filter(name = corp_name).exists()
  conditions = [cond1, cond2]
  return all(conditions)


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