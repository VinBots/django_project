from .abs_base_score import AbsBaseScore

from django.db.models import Q

from corporates.models.choices import Options
from corporates.models import NetZero


class Score_4_3(AbsBaseScore):
    """
    Does the net zero target include all the emissions?
    """

    def get_rating(self):

        valid_scope = [Options.SCOPE123_LOC, Options.SCOPE123_MKT]
        valid_scope_3_coverage = [Options.FULL]

        queryset = NetZero.objects.filter(
            Q(
                company__company_id=self.company_score.company.company_id,
                stated=Options.YES,
                coverage__in=valid_scope,
                scope_3_coverage__in=valid_scope_3_coverage,
            )
            | Q(
                company__company_id=self.company_score.company.company_id,
                ongoing=Options.YES,
                ongoing_coverage__in=valid_scope,
                scope_3_coverage__in=valid_scope_3_coverage,
            )
        )

        if queryset.exists():
            self.update_meta_value(
                {
                    "stated": queryset[0].stated,
                    "coverage": queryset[0].coverage,
                    "ongoing": queryset[0].ongoing,
                    "ongoing_coverage": queryset[0].ongoing_coverage,
                }
            )
            return Options.YES

    def map_rating_to_score(self):

        mapping_dict = {Options.YES: self.max_score}

        return mapping_dict.get(self.company_score.rating_value, 0)
