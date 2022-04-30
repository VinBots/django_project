import os

from corporates.models import (
    GHGQuant,
    TargetQuant,
    NetZero,
    LatestCompanyScore,
    Score,
    Corporate,
)
from corporates.models.choices import Options
from django.db.models import Q
from config import Config as c

BASE_DIR_XL_DB = os.path.join(c.DATA_FOLDER, c.XLS_FOLDER)
BASE_DIR_LIB = os.path.join(c.DATA_FOLDER, c.LIBRARY_FOLDER)

DIR_TO_CORP_CHARTS_TEMPLATES = "/corporates.html/charts/html_exports/"
DIR_TO_CORP_CHARTS_IMG = "django_project/images/charts/"


def check_validity(corp_name):

    cond1 = corp_name is not None
    cond2 = Corporate.objects.filter(name=corp_name).exists()
    conditions = [cond1, cond2]
    return all(conditions)


def get_path_to_chart(company_id, chart_name):
    path = os.path.join(
        DIR_TO_CORP_CHARTS_TEMPLATES, chart_name, chart_name + str(company_id) + ".html"
    )
    return path


def get_path_to_img(company_id, chart_name):
    path = os.path.join(
        DIR_TO_CORP_CHARTS_IMG, chart_name, chart_name + str(company_id) + ".jpeg"
    )

    return path


def get_targets_db(company_id):

    queryset = TargetQuant.objects.filter(
        Q(company__company_id=company_id) & Q(reduction_obj__gt=0)
    ).order_by("target_year", "reduction_obj")

    data_gross_abs = queryset.filter(type=Options.GROSS_ABSOLUTE).values()
    data_net_abs = queryset.filter(type=Options.NET_ABSOLUTE).values()

    data_net_zero_policy = NetZero.objects.filter(
        Q(company__company_id=company_id) & Q(ongoing=Options.YES)
    ).values()

    targets_dict = {
        Options.NET_ZERO: data_net_zero_policy,
        Options.GROSS_ABSOLUTE: data_gross_abs,
        Options.NET_ABSOLUTE: data_net_abs,
    }
    return targets_dict


def get_scores_details(company_id):

    metadata = LatestCompanyScore.objects.filter(company=company_id).values(
        "score__name",
        "score__max_score",
        "latest_score_value",
        "rating_value",
        "meta_value",
    )

    return {
        dict["score__name"]: {
            "value": dict.get("latest_score_value", ""),
            "max": dict.get("score__max_score", ""),
            "rating": dict.get("rating_value", ""),
            "meta": dict.get("meta_value", ""),
        }
        for dict in metadata
    }


def get_score_info():

    score_query = Score.objects.all().values()
    return {
        dict["name"]: {
            "max_score": dict.get("max_score", ""),
            "description": dict.get("description", ""),
        }
        for dict in score_query
    }


def get_score_data_db(company_id):

    transparency = LatestCompanyScore.objects.get_latest_company_score_value(
        company_id=company_id, score_name="Score_transparency"
    ).values_list("score_pct", flat=True)[0]
    commitments = LatestCompanyScore.objects.get_latest_company_score_value(
        company_id=company_id, score_name="Score_commitments"
    ).values_list("score_pct", flat=True)[0]
    results = LatestCompanyScore.objects.get_latest_company_score_value(
        company_id=company_id, score_name="Score_results"
    ).values_list("score_pct", flat=True)[0]

    score_data = {
        "rank": LatestCompanyScore.objects.get_rank(
            company_id=company_id, score_name="Score_total"
        ),
        "Score_transparency_pct": str(round(transparency, 1)),
        "Score_commitments_pct": str(round(commitments, 1)),
        "Score_results_pct": str(round(results, 1)),
        "Score_transparency_angle": transparency * 1.80,
        "Score_commitments_angle": commitments * 1.80,
        "Score_results_angle": results * 1.80,
    }

    return score_data


def get_last_3_years_ghg_db(company_id):

    reporting_year = GHGQuant.objects.get_last_reporting_year(company_id)
    if reporting_year:
        ghg_query = GHGQuant.objects.filter(
            company__company_id=company_id,
            source=Options.FINAL,
        ).order_by("-reporting_year")
        print(f"GHG QUERY = {ghg_query.values()}")

        property_list = []

        for obj in ghg_query:
            property_list.append(
                {
                    "scope_12_loc": obj.scope_12_loc,
                    "scope_12_mkt": obj.scope_12_mkt,
                    "scope_3_loc_agg": obj.scope_3_loc_agg,
                    "scope_3_mkt_agg": obj.scope_3_mkt_agg,
                    "scope_123_loc": obj.scope_123_loc,
                    "scope_123_mkt": obj.scope_123_mkt,
                }
            )
        zipped_dict = zip(ghg_query.values(), property_list)
        updated_ghg_query = []

        for dict1, dict2 in zipped_dict:
            dict1.update(dict2)
            updated_ghg_query.append(dict1)

        return updated_ghg_query
