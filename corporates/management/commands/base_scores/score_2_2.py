from .abs_base_score import AbsBaseScore

from corporates.models.choices import Options
from corporates.models import Verification
from corporates.utilities import last_2_years


class Score_2_2(AbsBaseScore):

    """
    Are S3 figures verified by a 3rd-party for the last reporting year?
    """

    def get_rating(self):

        valid_coverage = [Options.FULL, Options.PARTLY]

        queryset = Verification.objects.filter(
            company__company_id=self.company_score.company.company_id,
            reporting_year__in=last_2_years(),
            scope3_verification_completeness__in=valid_coverage,
        ).exclude(scope3_assurance_type=Options.NO)

        queryset_full = queryset.filter(scope3_verification_completeness=Options.FULL)
        queryset_partly = queryset.filter(
            scope3_verification_completeness=Options.PARTLY
        )
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
