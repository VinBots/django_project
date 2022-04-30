from pathlib import Path
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from corporates.models import Corporate, CorporateGrouping

from corporates.utilities import (
    get_targets_db,
    get_score_info,
    get_scores_details,
    check_validity,
    get_path_to_img,
    get_path_to_chart,
    get_score_data_db,
    get_last_3_years_ghg_db,
    get_library_queryset,
    file_exist,
)


from config import Config as c


def corporates_search(request, corp_name=None):

    if request.GET.get("query") is not None:
        path = reverse("corporates_home") + request.GET.get("query")
        return redirect(path)

    if check_validity(corp_name):

        selected_corp = Corporate.objects.get(name=corp_name)

        db = {
            "corp_scores_details": get_scores_details(
                company_id=selected_corp.company_id
            ),
            "score": get_score_info(),
            "score_data": get_score_data_db(company_id=selected_corp.company_id),
            "ghg": get_last_3_years_ghg_db(company_id=selected_corp.company_id),
            "targets": get_targets_db(company_id=selected_corp.company_id),
        }

        # library_corp = get_library_data(
        #     company_id=selected_corp.company_id,
        #     all_data=all_data[c.LIBRARY.LIST_CSV],
        #     db=True,
        # )

        corp_data = {
            "selected_corp": selected_corp,
            "db": db,
            "library_corp": {"ghg": get_library_queryset(selected_corp.company_id)},
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
                "corporates_names": Corporate.objects.filter(
                    company_id__in=CorporateGrouping.objects.get_sp100_company_ids()
                ).all(),
                "random_logos": Corporate.objects.random(),
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
            "corporates_names": Corporate.objects.filter(
                company_id__in=CorporateGrouping.objects.get_sp100_company_ids()
            ).all(),
            "random_logos": Corporate.objects.random(),
        },
    )


def show_html(request, folder_name=None, file_name=None):

    DIR_TO_CORP_CHARTS_TEMPLATES = (
        "templates/django_project/corporates/charts/html_exports/"
    )

    path = os.path.join(
        settings.BASE_DIR, DIR_TO_CORP_CHARTS_TEMPLATES, folder_name, file_name
    )

    return render(
        request,
        "django_project/corporates/show_interactive.html",
        {
            "path": path,
        },
    )
