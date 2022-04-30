from .abs_base_score import AbsBaseScore

from django.db.models import Q

from corporates.models.choices import Options
from corporates.models import NetZero


class Score_4_1(AbsBaseScore):
    """
    Does the net 0 target include a statement of a generally-accepted net zero emission target by 2050?
    """

    def get_rating(self):

        queryset = NetZero.objects.filter(
            Q(
                company__company_id=self.company_score.company.company_id,
                stated=Options.YES,
            )
            | Q(
                company__company_id=self.company_score.company.company_id,
                already_reached=Options.YES,
                ongoing=Options.YES,
            )
        )

        if queryset.exists():
            self.update_meta_value({"Number of Net Zero records": queryset.count()})
            return Options.YES

    def map_rating_to_score(self):

        mapping_dict = {Options.YES: self.max_score}

        return mapping_dict.get(self.company_score.rating_value, 0)
