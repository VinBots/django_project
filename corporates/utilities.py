import os
from datetime import date
import pandas as pd

from django.conf import settings
from django.db.models import Q

from corporates.models.ghg import GHGQuant
from corporates.models.metrics import CalcMetrics
from corporates.models.targets import TargetQuant
from corporates.models.netzero import NetZero
from corporates.models.scores import LatestCompanyScore, Score
from corporates.models.corp import Corporate
from corporates.models.verification import Verification
from corporates.models.external_sources.cdp import CDP
from corporates.models.general import GeneralInfo


from corporates.models.choices import Options

BASE_DIR_XL_DB = settings.EXCEL_DB_FOLDER
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
        "score_value",
        "rating_value",
        "meta_value",
    )

    return {
        dict["score__name"]: {
            "value": dict.get("score_value", ""),
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


def get_last_x_reporting_years(company_id, x=3):

    last_reporting_year = GHGQuant.objects.get_last_reporting_year(company_id)
    if last_reporting_year:
        return [
            str(year)
            for year in range(
                int(last_reporting_year), int(last_reporting_year) - x, -1
            )
        ]


def get_last_3_years_ghg_db(company_id):

    last_3_years = get_last_x_reporting_years(company_id, x=3)
    if last_3_years:
        ghg_query = GHGQuant.objects.filter(
            company__company_id=company_id,
            reporting_year__in=last_3_years,
            source=Options.FINAL,
        ).order_by("-reporting_year")

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


def get_last_3_years_estimates_db(company_id):

    last_3_years = get_last_x_years(x=3)
    if last_3_years:
        estimates_query = (
            CalcMetrics.objects.filter(
                company__company_id=company_id,
                year__in=last_3_years,
                metrics="total_ghg_estimate",
            )
            .distinct("year")
            .order_by("-year", "-last_update")
        )
        res = add_method_description(estimates_query.values())
        return res


def add_method_description(query_results):

    for result in query_results:
        method_description = Options.CO2_ESTIMATES_METHODS_DESCRIPTION.get(
            result["method"], "other"
        )
        result.update({"method_description": method_description})
    return query_results


def get_last_x_years(x=2):
    current_year = date.today().year
    return [str(int(current_year) - offset) for offset in range(1, x + 1)]


def target_statement_builder():

    """
    {company_name} committed to {verb = reduce/increase} {by/to} {percentage/value} its {gross/net} emissions covering {coverage} by {target_year} vs. {baseline_year}.
    This target is validated by SBTi (status). Its first year of measurement is {start_year}
    """
    pass


def get_forward_looking_reduction(
    last_reporting_year, last_reporting_year_ghg, baseline, reduction_obj, target_year
):
    """
    Calculates the forward-looking target reduction by year based on a stated target
    and the latest GHG emissions. See definition in methodology.
    """

    target_ghg = baseline * (1 - (reduction_obj / 100))
    forward_looking_reduction = (1 - (target_ghg / last_reporting_year_ghg)) * 100
    period = int(target_year) - int(last_reporting_year)

    return forward_looking_reduction / period


def to_pct(df, field, decimal=1):
    """Converts a field into numeric, multiply by 100 and rounded - used for percentage"""
    df.loc[:, field] = pd.to_numeric(df[field], errors="coerce") * 100
    df.loc[:, field] = df[field].round(decimal)
    return df


# def get_library_data(company_id, all_data=None, db=False):

#     dict = {}
#     fields = [c.LIBRARY.SUB_FOLDER_NAME, c.LIBRARY.FILENAME, c.LIBRARY.DESC]

#     if not db:
#         cond1 = all_data[c.FIELDS.COMPANY_ID] == company_id
#         for folder_name, category in c.LIBRARY.CATEGORIES_DESC.items():
#             cond2 = all_data[c.LIBRARY.SUB_FOLDER_NAME] == folder_name
#             filter_conditions = cond1 & cond2
#             record_data = all_data.loc[filter_conditions].sort_values(
#                 [c.LIBRARY.YEAR, c.LIBRARY.PART], ascending=[False, True]
#             )
#             record = record_data[fields].to_dict("records")
#             if len(record) > 0:
#                 dict[category] = record
#     else:

#         dict = {"queryset": get_library_queryset(company_id)}

#     return dict


def get_library_queryset(company_id, category="cdp"):

    category_to_query_map = {
        "cdp": CDP.objects.filter(company_id=company_id).order_by("-reporting_year"),
        "targets": TargetQuant.objects.filter(company_id=company_id).order_by(
            "target_year"
        ),
        "ghg": GHGQuant.objects.filter(company_id=company_id).order_by(
            "-reporting_year"
        ),
        "verif": Verification.objects.filter(company_id=company_id).order_by(
            "-reporting_year"
        ),
        "sust": GeneralInfo.objects.filter(company_id=company_id).order_by("-year"),
    }

    return category_to_query_map.get(category)


# def queryset_to_dict(queryset):
#     all_records = []
#     fields = ["upload_1", "upload_2", "upload_3", "upload_4", "upload_5"]
#     full_list = queryset.values()
#     all_records = [
#         {
#             "folder_name": "ghg2",
#             "filename": os.path.basename(record[field]),
#             "desc": f"{record['source_id']}-{record['reporting_year']}",
#         }
#         for record in full_list
#         for field in fields
#         if record[field]
#     ]
#     return all_records


# def get_all_data_from_csv(sheet_names, folder=BASE_DIR_XL_DB):

#     pd_dict = {}
#     for sheetname in sheet_names:
#         csv_path =


#         os.path.join(folder, sheetname + ".csv")
#         pd_dict[sheetname] = pd.read_csv(csv_path)
#     return pd_dict


def file_exist(path_name):

    path = os.path.join(settings.BASE_DIR, "static", path_name)
    return os.path.isfile(path)


def get_company_id_from_name(company_name):

    return Corporate.objects.filter(name=company_name).values_list("company_id")[0][0]
