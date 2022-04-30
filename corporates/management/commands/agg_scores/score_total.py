from .abs_agg_score import AbsAggScore
from django.db.models import Q, Sum
from corporates.models import Score, LatestCompanyScore


class Score_total(AbsAggScore):
    """ """

    def get_rating(self):

        scores_list = ["Score_" + str(x) for x in range(1, 11)]

        score_filter = Q(score__name__in=scores_list)
        queryset = LatestCompanyScore.objects.filter(
            Q(company__company_id=self.company_score.company.company_id), score_filter
        ).aggregate(result=Sum("latest_score_value"))

        if queryset:
            return queryset.get("result", 0)
