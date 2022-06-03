from .abs_base_score import AbsBaseScore

import numpy as np

from corporates.models import MSCI


class Score_10_1(AbsBaseScore):
    """
    Are the 15 categories disclosed? Total scope 3 can be aggregated or details are provided
    in the CDP report (link to the questionnaire to be provided. Link to CDP website is not enough)
    """

    SCORES_TABLES = {
        "intervals": [0, 1.5, 2.0, 2.5, 3.0, 4.0],
        "scores": [1, 1, 0.75, 0.50, 0.25, 0.0, 0.0],
    }

    def get_rating(self):

        """
        Is the company aligned with global climate targets?
        """

        queryset = MSCI.objects.filter(
            company__company_id=self.company_score.company.company_id,
        ).order_by("-last_update")

        if queryset.exists():
            return str(queryset[0].ITR)

    def map_rating_to_score(self):

        if not self.is_float(self.company_score.rating_value):
            return 0.0

        intervals = self.SCORES_TABLES.get("intervals")
        idx = np.searchsorted(intervals, float(self.company_score.rating_value))

        return self.SCORES_TABLES.get("scores")[idx] * self.max_score
