from .abs_base_score import AbsBaseScore
from corporates.models.external_sources.sbti import SBTI


class Score_7_1(AbsBaseScore):
    """
    What type of science-based target (as validated by SBTi) did the company commit to?
    """

    SCORES_TABLES = {
        "Targets Set 1.5°C": 1.0,
        "Targets Set Well-below 2°C": 0.75,
        "Targets Set 2°C": 0.5,
        "Committed ": 0.25,
    }

    def get_rating(self):

        # valid_SBTI = [valid_sbti for (valid_sbti, _) in Options.SBTI_CHOICES]

        queryset = SBTI.objects.filter(
            company__company_id=self.company_score.company.company_id
        ).order_by("-last_update")

        if queryset.exists():
            return queryset[0].status + " " + queryset[0].classification

    def map_rating_to_score(self):
        return (
            self.SCORES_TABLES.get(self.company_score.rating_value, 0) * self.max_score
        )
