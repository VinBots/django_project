import abc
from typing import Dict

from django.db.models import Q, Sum

from corporates.models import Score, LatestCompanyScore


class AbsAggScore(abc.ABC):
    def __init__(self, score_name: str):
        self.score_name = score_name
        self.company_score: LatestCompanyScore = None
        self.score_filter = None

    def message(self) -> None:
        print(
            f"Company: {self.company_score.company.name}: {self.company_score.score_value}pts [{self.company_score.score.name}]"
        )

    def filter_sum(self, score_number):
        score_filter = Q(score__name__startswith="Score_" + str(score_number) + "_")
        queryset = LatestCompanyScore.objects.filter(
            Q(company__company_id=self.company_score.company.company_id), score_filter
        ).aggregate(result=Sum("latest_score_value"))

        if queryset:
            # self.update_meta_value({"Count": len(queryset)})
            return queryset.get("result", 0)

    def map_rating_to_score(self):

        # mapping_dict = {Options.YES: self.max_score}

        return (
            self.company_score.rating_value
        )  # mapping_dict.get(self.company_score.rating_value, 0)

    @abc.abstractmethod
    def get_rating(self) -> str:
        pass

    # @abc.abstractmethod
    # def map_rating_to_score(self, rating: str) -> float:
    #     pass

    def update_meta_value(self, meta_data: Dict) -> Dict:
        if self.company_score:
            self.company_score.meta_value.update(meta_data)

    def get_max_score(self, score_name: str) -> float:

        return Score.objects.get_max_score(score_name)

    def get_blank_score(self, company_id: int) -> LatestCompanyScore:

        return LatestCompanyScore().get_blank_score(company_id, self.score_name)

    def get_score(self, company_id: int) -> float:

        self.company_score = self.get_blank_score(company_id)
        self.company_score.rating_value = self.get_rating()

        self.max_score = self.get_max_score(self.company_score.score.name)

        if self.company_score.rating_value:
            self.company_score.latest_score_value = self.map_rating_to_score()

        if self.max_score > 0:
            self.company_score.score_pct = (
                self.company_score.latest_score_value / self.max_score
            ) * 100

        return self.company_score

    def is_float(self, element: str) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False
