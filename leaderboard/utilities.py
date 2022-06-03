from django.db.models import F, Window, Subquery, OuterRef
from django.db.models.functions import Rank

from corporates.models import LatestCompanyScore, CorporateGrouping


def get_scores_db(corp_number=None, top_rank=True):

    rank_by_score = Window(
        expression=Rank(),
        partition_by=F("score"),
        order_by=F("score_value").desc(),
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
                sub_query_transparency.values("score_value")[:1]
            ),
            Score_commitments=Subquery(sub_query_commitments.values("score_value")[:1]),
            Score_results=Subquery(sub_query_results.values("score_value")[:1]),
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
    return result
