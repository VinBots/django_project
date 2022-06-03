from .abs_base_score import AbsBaseScore

from corporates.models.choices import Options
from corporates.models import Verification
from corporates.utilities import get_last_x_years


class Score_1_2(AbsBaseScore):
    """
    Are S1+S2 figures verified by a 3rd-party for the last reporting year?
    """

    def get_rating(self):

        queryset = Verification.objects.filter(
            company__company_id=self.company_score.company.company_id,
            reporting_year__in=get_last_x_years(x=2),
            scope12_verification_completeness=Options.FULL,
        ).exclude(scope12_assurance_type=Options.NO)

        if queryset.exists():
            self.update_meta_value(
                {"Number of GHG Inventory verified": queryset.count()}
            )
            return Options.YES

    def map_rating_to_score(self):

        mapping_dict = {Options.YES: self.max_score}

        return mapping_dict.get(self.company_score.rating_value, 0)
