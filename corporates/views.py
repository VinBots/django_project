from django.shortcuts import render, redirect
from corporates.models import Corporate

# Create your views here.

def home(request):
  return redirect('main_home')

def corporates_search(request, corp_name=None):
    
  if check_validity(corp_name):
    corp_data = {
    "corp_name": corp_name,
    }
    return render (request, "django_project/corporates/main.html", corp_data)
  else:
    return redirect('main_home')

def check_validity(corp_name):

  cond1 = corp_name is not None
  #corporates_names = Corporate.objects.all()
  cond2 = Corporate.objects.filter(name = corp_name).exists()
  conditions = [cond1, cond2]
  return all(conditions)


def corporates_home(request):

  corp_name = request.POST["query"]
  if check_validity(corp_name):
    corp_data = {
    "corp_name": corp_name,
    }
    return render (request, "django_project/corporates/main.html", corp_data)
  else:
    return redirect('main_home')