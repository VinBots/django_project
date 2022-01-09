from django.shortcuts import render, redirect
from corporates.models import Corporate
from django.urls import reverse
from corporates.utilities import (
    get_library_data,
    get_path_to_chart,
    check_validity,
    get_ghg,
    get_path_to_img,
    get_score_data,
    get_scores_summary,
    get_targets,
    file_exist,
    get_scores_details,
    get_all_data_from_csv,
)
from django_project.utilities import get_random_logos
from pathlib import Path
import os
from config import Config as c


def corporates_search(request, corp_name=None):

    if request.GET.get("query") is not None:
        path = reverse("corporates_home") + request.GET.get("query")
        return redirect(path)

    if check_validity(corp_name):

        selected_corp = Corporate.objects.get(name=corp_name)
        sheet_names = [
            c.DATA_FROM_XLSX.GHG_QUANT,
            c.DATA_FROM_XLSX.CORP_SCORES,
            c.DATA_FROM_XLSX.SCORES_SUMMARY,
            c.DATA_FROM_XLSX.TARGETS_QUANT,
            c.DATA_FROM_XLSX.SCORES_DETAILS,
            c.LIBRARY.LIST_CSV,
            c.DATA_FROM_XLSX.REPORTING,
        ]

        all_data = get_all_data_from_csv(sheet_names)

        xls_corp = {
            "ghg": get_ghg(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.GHG_QUANT],
                reporting_year_data=all_data[c.DATA_FROM_XLSX.REPORTING],
            ),
            "score_data": get_score_data(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.CORP_SCORES],
            ),
            "corp_scores_summary": get_scores_summary(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.SCORES_SUMMARY],
            ),
            "corp_scores_details": get_scores_details(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.SCORES_DETAILS],
            ),
            "targets": get_targets(
                company_id=selected_corp.company_id,
                all_data=all_data[c.DATA_FROM_XLSX.TARGETS_QUANT],
            ),
        }

        library_corp = get_library_data(
            company_id=selected_corp.company_id, all_data=all_data[c.LIBRARY.LIST_CSV]
        )

        corp_data = {
            "selected_corp": selected_corp,
            "xls_corp": xls_corp,
            "library_corp": library_corp,
            "selected_corp_bullet_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "bullet"),
                "img": get_path_to_img(selected_corp.company_id, "bullet"),
            },
            "selected_corp_bubble_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "bubble"),
                "img": get_path_to_img(selected_corp.company_id, "bubble"),
                "exist": file_exist(
                    get_path_to_img(selected_corp.company_id, "bubble")
                ),
            },
            "selected_corp_ghg_bar_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "ghg_bar"),
                "img": get_path_to_img(selected_corp.company_id, "ghg_bar"),
                "exist": file_exist(
                    get_path_to_img(selected_corp.company_id, "ghg_bar")
                ),
            },
            "selected_corp_ghg_scope3_pie_chart": {
                "html": get_path_to_chart(selected_corp.company_id, "ghg_pie_chart"),
                "img": get_path_to_img(selected_corp.company_id, "ghg_pie_chart"),
                "exist": file_exist(
                    get_path_to_img(selected_corp.company_id, "ghg_pie_chart")
                ),
            },
        }

        return render(request, "django_project/corporates/main.html", corp_data)
    else:
        return render(
            request,
            "django_project/corporates/home.html",
            {
                "error_msg": "No match found",
                "corporates_names": Corporate.objects.all(),
                "random_logos": get_random_logos(),
            },
        )


def corporates_home(request):

    if request.GET.get("query") is not None:
        path = reverse("corporates_home") + request.GET.get("query")
        return redirect(path)

    return render(
        request,
        "django_project/corporates/home.html",
        {
            "error_msg": "",
            "corporates_names": Corporate.objects.all(),
            "random_logos": get_random_logos(),
        },
    )


def show_html(request, folder_name=None, file_name=None):

    BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")

    DIR_TO_CORP_CHARTS_TEMPLATES = (
        "templates/django_project/corporates/charts/html_exports/"
    )

    path = os.path.join(BASE_DIR, DIR_TO_CORP_CHARTS_TEMPLATES, folder_name, file_name)

    return render(
        request,
        "django_project/corporates/show_interactive.html",
        {
            "path": path,
        },
    )
