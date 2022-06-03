from .abs_base_score import AbsBaseScore

from corporates.models.choices import Options
from corporates.models import Verification
from corporates.utilities import get_last_x_years


class Score_2_1(AbsBaseScore):
    """
    Are the 15 categories disclosed? Total scope 3 can be aggregated or details are provided
    in the CDP report (link to the questionnaire to be provided. Link to CDP website is not enough)
    """

    def get_rating(self):

        valid_coverage = [Options.FULL, Options.PARTLY]

        queryset = Verification.objects.filter(
            company__company_id=self.company_score.company.company_id,
            reporting_year__in=get_last_x_years(x=2),
            scope3_reporting_completeness__in=valid_coverage,
        )
        queryset_full = queryset.filter(scope3_reporting_completeness=Options.FULL)
        queryset_partly = queryset.filter(scope3_reporting_completeness=Options.PARTLY)

        if queryset_full.exists():
            self.update_meta_value({"Number of GHG Inventory": queryset_full.count()})
            return Options.FULL

        elif queryset_partly.exists():
            self.update_meta_value({"Number of GHG Inventory": queryset_partly.count()})
            return Options.PARTLY

    def map_rating_to_score(self):

        mapping_dict = {
            Options.FULL: self.max_score,
            Options.PARTLY: self.max_score * 0.5,
        }

        return mapping_dict.get(self.company_score.rating_value, 0)
