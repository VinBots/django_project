import os, pathlib, math
from datetime import date

import pandas as pd

from corporates.models import Corporate
from corporates.models.ghg import GHGQuant
from django.conf import settings
from config import Config as c

BASE_DIR_XL_DB = os.path.join(c.DATA_FOLDER, c.XLS_FOLDER)
BASE_DIR_LIB = os.path.join(c.DATA_FOLDER, c.LIBRARY_FOLDER)

DIR_TO_CORP_CHARTS_TEMPLATES = "/corporates.html/charts/html_exports/"
DIR_TO_CORP_CHARTS_IMG = "django_project/images/charts/"

# def get_score_data(company_id, all_data=None):

#     score_record_data = all_data[all_data[c.FIELDS.COMPANY_ID] == company_id]
#     num_cols = c.SCORES.CATEGORIES + [c.SCORES.TOTAL, c.SCORES.RANK]

#     score_record_data[num_cols] = score_record_data[num_cols].apply(pd.to_numeric)

#     score_data = {
#         "score": score_record_data[c.SCORES.TOTAL].values[0],
#         "rank": score_record_data[c.SCORES.RANK].values[0],
#         "transp_ratio": str(
#             round(score_record_data[c.SCORES.TRANSPARENCY_RATIO].values[0] * 100, 1)
#         ),
#         "transp_angle": score_record_data[c.SCORES.TRANSPARENCY_RATIO].values[0] * 180,
#         "comm_ratio": str(
#             round(score_record_data[c.SCORES.COMMITMENTS_RATIO].values[0] * 100, 1)
#         ),
#         "comm_angle": score_record_data[c.SCORES.COMMITMENTS_RATIO].values[0] * 180,
#         "actions_ratio": str(
#             round(score_record_data[c.SCORES.ACTIONS_RATIO].values[0] * 100, 1)
#         ),
#         "actions_angle": score_record_data[c.SCORES.ACTIONS_RATIO].values[0] * 180,
#     }

#     return score_data


# def get_score_data_db(company_id):

#     transparency = LatestCompanyScore.objects.get_latest_company_score_value(
#         company_id=company_id, score_name="Score_transparency"
#     ).values_list("score_pct", flat=True)[0]
#     commitments = LatestCompanyScore.objects.get_latest_company_score_value(
#         company_id=company_id, score_name="Score_commitments"
#     ).values_list("score_pct", flat=True)[0]
#     results = LatestCompanyScore.objects.get_latest_company_score_value(
#         company_id=company_id, score_name="Score_results"
#     ).values_list("score_pct", flat=True)[0]

#     score_data = {
#         "rank": LatestCompanyScore.objects.get_rank(
#             company_id=company_id, score_name="Score_total"
#         ),
#         "Score_transparency_pct": str(round(transparency, 1)),
#         "Score_commitments_pct": str(round(commitments, 1)),
#         "Score_results_pct": str(round(results, 1)),
#         "Score_transparency_angle": transparency * 1.80,
#         "Score_commitments_angle": commitments * 1.80,
#         "Score_results_angle": results * 1.80,
#     }

#     return score_data


# def get_scores_summary(company_id, all_data=None):

#     scores_summary_data = all_data[all_data[c.FIELDS.COMPANY_ID] == company_id]
#     score_data_dict = c.SCORES.STRUCTURE

#     for category in score_data_dict.keys():
#         for score in score_data_dict[category]["details"]:
#             score["score"] = scores_summary_data[score["field"]].values[0]
#         score_data_dict[category]["total"]["score"] = scores_summary_data[
#             score_data_dict[category]["total"]["field"]
#         ].values[0]

#     return score_data_dict


def to_pct(df, field, decimal=1):
    """Converts a field into numeric, multiply by 100 and rounded - used for percentage"""
    df.loc[:, field] = pd.to_numeric(df[field], errors="coerce") * 100
    df.loc[:, field] = df[field].round(decimal)
    return df


# def get_scores_details(company_id, all_data=None):
#     """Returns detailed score data"""
#     scores_details_data = all_data[all_data[c.FIELDS.COMPANY_ID] == company_id].fillna(
#         "NA"
#     )
#     pct_fields = c.SCORES.PCT_FIELDS
#     for field_name in pct_fields:
#         scores_details_data = to_pct(scores_details_data, field_name)

#     scores_details_data = scores_details_data.fillna("NA")

#     return scores_details_data.to_dict(orient="records")[0]


def get_library_data(company_id, all_data=None, db=False):

    dict = {}
    fields = [c.LIBRARY.SUB_FOLDER_NAME, c.LIBRARY.FILENAME, c.LIBRARY.DESC]

    if not db:
        cond1 = all_data[c.FIELDS.COMPANY_ID] == company_id
        for folder_name, category in c.LIBRARY.CATEGORIES_DESC.items():
            cond2 = all_data[c.LIBRARY.SUB_FOLDER_NAME] == folder_name
            filter_conditions = cond1 & cond2
            record_data = all_data.loc[filter_conditions].sort_values(
                [c.LIBRARY.YEAR, c.LIBRARY.PART], ascending=[False, True]
            )
            record = record_data[fields].to_dict("records")
            if len(record) > 0:
                dict[category] = record
    else:

        dict = {"queryset": get_library_queryset(company_id)}

    print(dict)
    return dict


def get_library_queryset(company_id):

    queryset = GHGQuant.objects.filter(company_id=company_id).order_by(
        "-reporting_year"
    )

    return queryset


def queryset_to_dict(queryset):
    all_records = []
    fields = ["upload_1", "upload_2", "upload_3", "upload_4", "upload_5"]
    full_list = queryset.values()
    print(full_list)
    all_records = [
        {
            "folder_name": "ghg2",
            "filename": os.path.basename(record[field]),
            "desc": f"{record['source_id']}-{record['reporting_year']}",
        }
        for record in full_list
        for field in fields
        if record[field]
    ]
    print(f"All the records are {all_records}")
    return all_records


# def get_targets(company_id, all_data=None):

#     targets_record_data = all_data.loc[
#         (all_data[c.FIELDS.COMPANY_ID] == company_id)
#         & (
#             all_data[c.TARGETS.SOURCES.FIELD].isin(
#                 [
#                     c.TARGETS.SOURCES.SBTI,
#                     c.TARGETS.SOURCES.PUBLIC,
#                     c.TARGETS.SOURCES.CDP,
#                 ]
#             )
#         )
#     ]
#     targets_select_data = targets_record_data[
#         [
#             c.TARGETS.TYPE.FIELD,
#             c.TARGETS.SCOPE,
#             c.TARGETS.COV_S3,
#             c.TARGETS.REDUCTION_OBJ,
#             c.TARGETS.BASE_YEAR,
#             c.TARGETS.TARGET_YEAR,
#         ]
#     ]
#     targets_select_data.loc[:, c.TARGETS.REDUCTION_OBJ] = (
#         pd.to_numeric(targets_select_data[c.TARGETS.REDUCTION_OBJ], errors="coerce")
#         * 100
#     )
#     data_gross_abs = json.loads(
#         targets_select_data.loc[
#             (targets_select_data[c.FIELDS.TARGET_TYPE] == c.TARGETS.TYPE.GROSS_ABSOLUTE)
#         ]
#         .sort_values(by=c.TARGETS.SCOPE)
#         .reset_index()
#         .to_json(orient="records")
#     )
#     data_net_abs = json.loads(
#         targets_select_data.loc[
#             (targets_select_data[c.FIELDS.TARGET_TYPE] == c.TARGETS.TYPE.NET_ABSOLUTE)
#         ]
#         .sort_values(by=c.TARGETS.SCOPE)
#         .reset_index()
#         .to_json(orient="records")
#     )
#     data_net_zero_policy = json.loads(
#         targets_select_data.loc[
#             (targets_select_data[c.FIELDS.TARGET_TYPE] == c.TARGETS.TYPE.NET0_POLICY)
#         ]
#         .sort_values(by=c.TARGETS.SCOPE)
#         .reset_index()
#         .to_json(orient="records")
#     )

#     targets_dict = {
#         c.TARGETS.TYPE.NET0_POLICY: data_net_zero_policy,
#         c.TARGETS.TYPE.GROSS_ABSOLUTE: data_gross_abs,
#         c.TARGETS.TYPE.NET_ABSOLUTE: data_net_abs,
#     }

#     return targets_dict


# def get_last_3_years_ghg_db(company_id):

#     reporting_year = GHGQuant.objects.get_last_reporting_year(company_id)
#     if reporting_year:
#         ghg_query = GHGQuant.objects.filter(
#             company__company_id=company_id,
#             source=Options.FINAL,
#         ).order_by("-reporting_year")
#         print(f"GHG QUERY = {ghg_query.values()}")

#         property_list = []

#         for obj in ghg_query:
#             property_list.append(
#                 {
#                     "scope_12_loc": obj.scope_12_loc,
#                     "scope_12_mkt": obj.scope_12_mkt,
#                     "scope_3_loc_agg": obj.scope_3_loc_agg,
#                     "scope_3_mkt_agg": obj.scope_3_mkt_agg,
#                     "scope_123_loc": obj.scope_123_loc,
#                     "scope_123_mkt": obj.scope_123_mkt,
#                 }
#             )
#         zipped_dict = zip(ghg_query.values(), property_list)
#         updated_ghg_query = []

#         for dict1, dict2 in zipped_dict:
#             dict1.update(dict2)
#             updated_ghg_query.append(dict1)

#         return updated_ghg_query


# def get_ghg(company_id, all_data, reporting_year_data):

#     fields = [
#         c.FIELDS.REPORTING_YEAR,
#         c.GHG.SOURCES.FIELD,
#         c.GHG.SCOPE1,
#         c.GHG.SCOPE2_LOC,
#         c.GHG.SCOPE2_MKT,
#         c.GHG.SCOPE3,
#         c.GHG.TOTAL,
#     ]
#     last_reporting_year = get_last_reporting_year(reporting_year_data, company_id)

#     cond1 = all_data[c.FIELDS.COMPANY_ID] == company_id
#     cond2 = all_data[c.GHG.SOURCES.FIELD].isin([c.GHG.SOURCES.FINAL])
#     cond3 = all_data[c.FIELDS.REPORTING_YEAR] <= last_reporting_year
#     cond4 = all_data[c.FIELDS.REPORTING_YEAR] >= last_reporting_year - 2
#     filter_conditions = cond1 & cond2 & cond3 & cond4

#     record_data = (
#         all_data.loc[filter_conditions]
#         .reset_index()
#         .sort_values(c.FIELDS.REPORTING_YEAR, ascending=False)
#     )
#     record_data = record_data[fields]  # specific fields only
#     dict = (
#         record_data.loc[record_data[c.GHG.SOURCES.FIELD].isin([c.GHG.SOURCES.FINAL])]
#         .reset_index()
#         .to_dict()
#     )

#     for each_dict in dict:
#         for key, value in dict[each_dict].items():
#             if isinstance(value, float):
#                 dict[each_dict][key] = int(value)

#     return {"final": dict}


def get_all_data_from_csv(sheet_names):

    pd_dict = {}
    for sheetname in sheet_names:
        csv_path = os.path.join(BASE_DIR_XL_DB, sheetname + ".csv")
        pd_dict[sheetname] = pd.read_csv(csv_path)
    return pd_dict


def get_last_reporting_year(all_data, company_id):

    last_reporting_year = all_data.loc[all_data[c.FIELDS.COMPANY_ID] == company_id][
        [c.FIELDS.LAST_REPORTING_YEAR]
    ].iloc[0, 0]
    return last_reporting_year


def ghg_format(number):
    if math.isnan(number):
        return "not found"
    else:
        return f"{float(number):,.0f}"


def file_exist(path_name):

    path = os.path.join(settings.BASE_DIR, "static", path_name)
    return os.path.isfile(path)


def get_company_id_from_name(company_name):

    return Corporate.objects.filter(name=company_name).values_list("company_id")[0][0]


def user_directory_path(instance, filename):

    if instance._meta.model.__name__ == "GeneralInfo":
        folder = "general2"

    # FORMAT '[reporting_year]_[company_name]_[source]_[submitter]
    filename = f"{folder}/{instance.reporting_year}_{instance.company.name}\
        _{instance.source}_{instance.submitter.username}\
            {pathlib.Path(filename).suffix}"
    print(f"FILE TO SAVE: {filename}")
    return filename


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


def last_2_years():
    current_year = date.today().year
    return [
        str(int(current_year) - 1),
        str(int(current_year) - 2),
    ]


def target_statement_builder():

    """
    {company_name} committed to {verb = reduce/increase} {by/to} {percentage/value} its {gross/net} emissions covering {coverage} by {target_year} vs. {baseline_year}.
    This target is validated by SBTi (status). Its first year of measurement is {start_year}
    """
    pass
