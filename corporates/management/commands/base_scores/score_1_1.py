from .abs_base_score import AbsBaseScore

from corporates.models.choices import Options
from corporates.models import Verification

from corporates.utilities import last_2_years


class Score_1_1(AbsBaseScore):
    """
    Are S1+S2 figures publicly-disclosed for the last reporting year and the preceding period?
    """

    def get_rating(self):

        queryset = Verification.objects.filter(
            company__company_id=self.company_score.company.company_id,
            scope12_reporting_2_years=Options.YES,
            reporting_year__in=last_2_years(),
        )

        if queryset.exists():
            self.update_meta_value({"Number of records found": queryset.count()})
            return Options.YES

    def map_rating_to_score(self):

        mapping_dict = {Options.YES: self.max_score}

        return mapping_dict.get(self.company_score.rating_value, 0)
