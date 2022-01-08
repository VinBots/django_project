from corporates.models import Corporate
from django.urls import reverse
from leaderboard.utilities import get_scores_xls
from django.shortcuts import render, redirect
from django_project.utilities import get_random_logos, get_top10_wo_zero, get_top5_transp_miss_cut
import os
from django.http import HttpResponse
from pathlib import Path
from django.core.files import File
from django_project.utilities import get_general_stats


def home(request):

  if request.GET.get("query") is not None:
    path = reverse('corporates_home') + request.GET.get("query")
    return redirect(path)

  corporates_names = Corporate.objects.all()
  pct_values = get_general_stats(['trust', 'commitments', 'science'])
  angle_deg = [str(pct_values[i] * 1.8) + "deg" for i in range(3)]

  return render (request, "django_project/home/main.html", {
    "corporates_names": corporates_names,
    "random_logos": get_random_logos(),
    "angle1":angle_deg[0],"value1":str(pct_values[0]),
    "angle2":angle_deg[1],"value2":str(pct_values[1]),
    "angle3":angle_deg[2],"value3":str(pct_values[2]),
    "top5_scores": get_scores_xls(corp_number=5, top_rank=True),
    "bottom5_scores": get_scores_xls(corp_number=5, top_rank=False),
    "top10_wo_zero" : get_top10_wo_zero()
    }
      )

def sectors(request, sector_name):

  sector_data = {
    "sector_name": sector_name,
    "sector_code": "xxxx"
  }
  return render (request, "django_project/sectors/main.html", sector_data)

def sectors_search(request):
  return render (request, "django_project/sectors/main.html")

def aboutus(request):
  return render (request, "django_project/aboutus/main.html")

def blog(request):

  return render (
    request,
    "django_project/blog/main.html",
    {
      "top5_mising_cut": get_top5_transp_miss_cut(),
    }
  )

def faq(request):
  return render (request, "django_project/faq/main.html")

def download_file (request, folder_name = '', file_name = ''):

    if file_name !='':
      BASE_DIR_LIB = os.path.join(Path(__file__).parent.parent.parent,'net0_docs','reports')
      filepath = os.path.join (BASE_DIR_LIB, folder_name, file_name)
      if os.path.exists(filepath):
        f = open(filepath, 'rb')
        pdfFile = File(f)
        response = HttpResponse(pdfFile.read())
        response['Content-Disposition'] = "attachment;filename=%s" % file_name
        return response
      else:
        return None
    else:
      return redirect(reverse('main_home'))