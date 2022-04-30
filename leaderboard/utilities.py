# from corporates.utilities import get_all_data_from_csv
import os
from pathlib import Path
import json
import pandas as pd
from config import Config as c
from corporates.models import LatestCompanyScore, CorporateGrouping
from django.db.models import F, Window, Q
from django.db.models.functions import Rank
from django.db.models import F, Window, Subquery, OuterRef

BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")


# def get_scores_xls(corp_number=None, top_rank=True):
#     """
#     Fetch companies information according to their score
#     By default, fetch all the companies in the database.
#     corp_number specifies the number of companies to return
#     if top_rank is set to True, it returns the top ranked companies
#     if top_rank is set to False, it returns the bottom ranked companies
#     """

#     all_data = get_all_data_from_csv(["corp_scores"])["corp_scores"]

#     max_rank = all_data[c.SCORES.RANK].max()
#     all_data[c.FIELDS.COMPANY_ID] = pd.to_numeric(
#         all_data[c.FIELDS.COMPANY_ID], downcast="integer"
#     )
#     all_data[c.SCORES.RANK] = pd.to_numeric(all_data[c.SCORES.RANK], downcast="integer")
#     all_data[c.SCORES.TRANSPARENCY_RATIO] = (
#         pd.to_numeric(all_data[c.SCORES.TRANSPARENCY_RATIO]) * 100
#     )
#     all_data[c.SCORES.COMMITMENTS_RATIO] = (
#         pd.to_numeric(all_data[c.SCORES.COMMITMENTS_RATIO]) * 100
#     )
#     all_data[c.SCORES.ACTIONS_RATIO] = (
#         pd.to_numeric(all_data[c.SCORES.ACTIONS_RATIO]) * 100
#     )

#     if not corp_number:
#         corp_number = max_rank

#     if top_rank:
#         all_data = all_data.loc[all_data[c.SCORES.RANK] <= corp_number].sort_values(
#             by=[c.SCORES.RANK]
#         )
#     else:
#         all_data = all_data.loc[
#             all_data[c.SCORES.RANK] > max_rank - corp_number
#         ].sort_values(by=[c.SCORES.RANK])

#     # parsing the DataFrame in json format.
#     json_records = all_data.reset_index().to_json(orient="records")
#     data = []
#     data = json.loads(json_records)
#     print(data)

#     return data


def get_scores_db(corp_number=None, top_rank=True):

    rank_by_score = Window(
        expression=Rank(),
        partition_by=F("score"),
        order_by=F("latest_score_value").desc(),
    )
    sub_query_transparency = LatestCompanyScore.objects.filter(
        company=OuterRef("company"), score__name="Score_transparency"
    )
    sub_query_commitments = LatestCompanyScore.objects.filter(
        company=OuterRef("company"), score__name="Score_commitments"
    )
    sub_query_results = LatestCompanyScore.objects.filter(
        company=OuterRef("company"), score__name="Score_results"
    )

    query = (
        LatestCompanyScore.objects.filter(
            company__in=CorporateGrouping.objects.get_sp100_company_ids(),
            score__name__in=["Score_total"],
        )
        .annotate(
            rank=rank_by_score,
            Score_transparency=Subquery(
                sub_query_transparency.values("latest_score_value")[:1]
            ),
            Score_commitments=Subquery(
                sub_query_commitments.values("latest_score_value")[:1]
            ),
            Score_results=Subquery(sub_query_results.values("latest_score_value")[:1]),
        )
        .order_by("rank")
    )
    result = query

    if top_rank:
        if corp_number:
            result = query[:corp_number]
    else:
        start_idx = query.count() - corp_number
        if start_idx > 0:
            result = query[start_idx:]
    print(result)
    return result
