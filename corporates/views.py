from django.shortcuts import render, redirect
from corporates.models import Corporate
from django.urls import reverse
from corporates.utilities import get_path_to_chart, check_validity, get_ghg_xls, get_path_to_img
from corporates.add_records import add_new_records
from django_project.utilities import get_random_logos


def corporates_search(request, corp_name=None):


  if request.GET.get("query") is not None:
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  if check_validity(corp_name):
    selected_corp = Corporate.objects.get(name=corp_name)
    xls_corp = {
      'ghg': get_ghg_xls(company_id=selected_corp.company_id)
    }

    corp_data = {
    "selected_corp": selected_corp,
    "xls_corp": xls_corp,
    "selected_corp_bullet_chart": {
      'html': get_path_to_chart(selected_corp.company_id, "bullet"),
      'img': ''
    },
    "selected_corp_bubble_chart": {
      'html': get_path_to_chart(selected_corp.company_id, "bubble"),
      'img': get_path_to_img (selected_corp.company_id, "bubble"),
    },
    "selected_corp_ghg_bar_chart": {
      'html': get_path_to_chart(selected_corp.company_id, "ghg_bar"),
      'img':'',
    },
    }
    
    return render (request, "django_project/corporates/main.html", corp_data)
  else:
    return render(
      request, 
      "django_project/corporates/home.html", 
      {"error_msg":"No match found",
      "corporates_names": Corporate.objects.all(),
      "random_logos": get_random_logos(),
      }
      )


def corporates_home(request):

  if request.GET.get("query") is not None:
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)
  
  #id_list = list(range(1, 101, 1))
  #add_new_records(id_list)
  return render(
    request,
    "django_project/corporates/home.html", 
    {
      "error_msg":"",
      "corporates_names": Corporate.objects.all(),
      "random_logos": get_random_logos(),
    }
    )