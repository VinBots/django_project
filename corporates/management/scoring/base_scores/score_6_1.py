from .abs_base_score import AbsBaseScore

from .score_6_x import get_rating_6_x, map_rating_6_x_to_score
from corporates.models.choices import Options


class Score_6_1(AbsBaseScore):
    """
    Calculates the forward-looking GHG% reduction
    for scope 1+2 and scope1+2+3

    Score: Linear from 0% (0 pts) to 5%+ per year
    """

    MAX_REDUCTION_6_x = 5

    def get_rating(self):

        valid_coverage = [
            Options.SCOPE12_LOC,
            Options.SCOPE12_MKT,
        ]
        valid_target_type = [Options.GROSS_ABSOLUTE]

        valid_target = {
            "scope_coverage__in": valid_coverage,
            "type__in": valid_target_type,
        }

        rating, meta_value = get_rating_6_x(
            self.company_score, valid_target=valid_target
        )
        self.update_meta_value(meta_value)
        if rating:
            return str(rating)

    def map_rating_to_score(self):
        return map_rating_6_x_to_score(self)
