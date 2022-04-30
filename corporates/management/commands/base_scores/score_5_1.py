from .abs_base_score import AbsBaseScore

from datetime import date

from django.db.models import Q

from corporates.models.choices import Options
from corporates.models import NetZero


class Score_5_1(AbsBaseScore):
    """
    Does the net 0 target include a statement of a generally-accepted net zero emission target by 2050?
    """

    NETZERO_YEAR_LIMIT = 2050

    def get_rating(self):

        valid_coverage = [
            Options.SCOPE12_LOC,
            Options.SCOPE12_MKT,
            Options.SCOPE123_LOC,
            Options.SCOPE123_MKT,
        ]

        ongoing_netzero_condition = Q(already_reached=Options.YES, ongoing=Options.YES)
        coverage_condition = Q(ongoing_coverage__in=valid_coverage)
        case1_queryset = NetZero.objects.filter(
            Q(company__company_id=self.company_score.company.company_id),
            ongoing_netzero_condition & coverage_condition,
        )

        coverage_condition = Q(coverage__in=valid_coverage)
        case2_queryset = NetZero.objects.filter(
            Q(company__company_id=self.company_score.company.company_id),
            Q(stated=Options.YES) & coverage_condition,
        ).order_by("target_year")

        if case1_queryset.exists():
            return "Net Zero Policy"

        elif case2_queryset.exists():
            return case2_queryset[0].target_year

    def map_rating_to_score(self):

        if self.company_score.rating_value == "Net Zero Policy":
            return self.max_score

        ref_year = int(date.today().year) - 1
        max_years = self.NETZERO_YEAR_LIMIT - int(date.today().year)

        result = 1 - ((int(self.company_score.rating_value) - ref_year) / max_years)

        return max([0, min([1, result])]) * self.max_score
