from .abs_base_score import AbsBaseScore

from corporates.models.choices import Options
from corporates.models import GHGQuant
from corporates.management.commands.base_scores.score_8and9 import (
    historical_perf_x,
    map_rating_to_score_8and9,
)


class Score_8_1(AbsBaseScore):
    """
    Calculates the forward-looking GHG% reduction
    for scope 1+2 and scope1+2+3

    Score: Linear from 0% (0 pts) to 5%+ per year
    """

    MAX_REDUCTION_6_x = 5

    def get_rating(self):

        valid_target_type = [Options.GROSS_ABSOLUTE]

        valid_coverage = [
            Options.SCOPE12_LOC,
            Options.SCOPE12_MKT,
        ]
        last_reporting_year = GHGQuant.objects.get_last_reporting_year(
            company_id=self.company_score.company.company_id
        )
        if last_reporting_year:
            valid_target_year = [
                str(x) for x in list(range(int(last_reporting_year) + 1, 2051))
            ]
        else:
            meta_value = {
                "error": f"The last reporting year could be found in the database"
            }
            self.update_meta_value(meta_value)
            return None

        valid_target = {
            "type__in": valid_target_type,
            "scope_coverage__in": valid_coverage,
            "target_year__in": valid_target_year,
        }

        rating, meta_value = historical_perf_x(
            score_value=self.company_score, valid_target=valid_target
        )
        self.update_meta_value(meta_value)
        if rating:
            return str(rating)

    def map_rating_to_score(self):
        return map_rating_to_score_8and9(self)
