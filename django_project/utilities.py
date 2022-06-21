import os
import json
from django.conf import settings

from corporates.models.scores import LatestCompanyScore


def get_top10_wo_zero():

    filename = os.path.join(
        settings.BASE_DIR, "static", "data", "top10_wo_net_zero.json"
    )
    with open(filename) as f:
        data = json.load(f)
        for company_dict in data:
            company_dict.update(
                {
                    "rank": LatestCompanyScore.objects.get_rank(
                        company_id=company_dict["company_id"], score_name="Score_total"
                    )
                }
            )
    return data


def get_top5_transp_miss_cut():

    filename = os.path.join(
        settings.BASE_DIR,
        "static",
        "data",
        "django_project",
        "top5_transp_miss_cut.json",
    )
    with open(filename) as f:
        data = json.load(f)
    return data


def get_general_stats(indicators):
    path = os.path.join(settings.DATA_FOLDER, "home_page", "general_stats.json")

    with open(path) as json_file:
        dict = json.load(json_file)

    list_ind = [dict[indicator] for indicator in indicators]
    for ind_dict in list_ind:
        ind_dict["angle"] = str(ind_dict["value"] * 1.8) + "deg"

    return list_ind
