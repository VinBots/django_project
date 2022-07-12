import abc
from typing import Dict

from corporates.models import Score, CompanyScore


class AbsBaseScore(abc.ABC):
    def __init__(self, score_name: str):
        self.score_name = score_name
        self.company_score: CompanyScore = None

    def message(self) -> None:
        print(
            f"Company: {self.company_score.company.name}: {self.company_score.score_value}pts [{self.company_score.score.name}]"
        )

    @abc.abstractmethod
    def get_rating(self) -> str:
        pass

    @abc.abstractmethod
    def map_rating_to_score(self, rating: str) -> float:
        pass

    def update_meta_value(self, meta_data: Dict) -> Dict:
        if self.company_score:
            self.company_score.meta_value.update(meta_data)

    def get_max_score(self, score_name: str) -> float:

        return Score.objects.get_max_score(score_name)

    def get_blank_score(self, company_id: int) -> CompanyScore:

        return CompanyScore().get_blank_score(company_id, self.score_name)

    def get_score(self, company_id: int, version) -> float:

        self.company_score = self.get_blank_score(company_id)
        self.company_score.version = version
        self.company_score.rating_value = self.get_rating()
        if self.company_score.rating_value:
            self.max_score = self.get_max_score(self.company_score.score.name)
            self.company_score.score_value = self.map_rating_to_score()

        return self.company_score

    def is_float(self, element: str) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False
