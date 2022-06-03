from .abs_base_score import AbsBaseScore

from corporates.models import TargetQuant


class Score_4_2(AbsBaseScore):
    """
    Does the net zero target include an intermediate target by 2030?
    conda ac"""

    ST_TARGET_YEAR_LIMIT = 2030

    def get_rating(self):

        queryset = TargetQuant.objects.get_earliest_highest(
            company_id=self.company_score.company.company_id,
            valid_target=None,
        )
        if not queryset.exists():
            self.update_meta_value({"error": "No target found"})
            return None

        self.update_meta_value({"Number of targets found": queryset.count()})
        return str(queryset[0].target_year)

    def map_rating_to_score(self):

        if int(self.company_score.rating_value) <= self.ST_TARGET_YEAR_LIMIT:
            return self.max_score
        else:
            return 0
