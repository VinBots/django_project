from .abs_base_score import AbsBaseScore

from corporates.models.choices import Options
from corporates.models import CDP
from corporates.utilities import get_last_x_years


class Score_3_1(AbsBaseScore):
    """
    Are the 15 categories disclosed? Total scope 3 can be aggregated or details are provided
    in the CDP report (link to the questionnaire to be provided. Link to CDP website is not enough)
    """

    SCORES_TABLES = {
        "a": 1.0,
        "a-": 0.9,
        "b": 0.8,
        "b-": 0.7,
        "c": 0.6,
        "c-": 0.5,
        "d": 0.4,
        "d-": 0.3,
        "f": 0.0,
    }

    def get_rating(self):

        valid_cdp_scores = [cdp_score[0] for cdp_score in Options.CDP_SCORE_OPTIONS]

        queryset = CDP.objects.filter(
            company__company_id=self.company_score.company.company_id,
            questionnaire_year__in=get_last_x_years(x=2),
            score__in=valid_cdp_scores,
        ).order_by("questionnaire_year")

        if queryset.exists():
            return queryset[0].score

    def map_rating_to_score(self):

        return (
            self.SCORES_TABLES.get(self.company_score.rating_value, 0) * self.max_score
        )
