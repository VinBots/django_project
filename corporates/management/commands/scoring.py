from corporates.models import CompanyScore
from .base_score_factory import BaseScoreFactory
from .agg_score_factory import AggScoreFactory


class Scoring:
    """
    Retrieves or calculates the scores for a list of companies
    """

    def __init__(self, company_ids, score_name):
        self.company_ids = company_ids
        self.score_name = score_name
        self.data_check = self.data_check_test()

        self.saved_scores_count = 0

    def get_implemented_ref(self):
        pass

    def get_all_scores(self):
        for ref in self.get_implemented_ref():
            self.get_score(ref=ref)

    def check_companies(self):
        return True

    def check_score_name(self):
        return True

    def data_check_test(self):
        self.valid_companies = self.check_companies()
        self.valid_score_name = self.check_score_name()
        return self.valid_companies and self.valid_score_name

    def process_scores(self):

        if self.data_check:
            factory = BaseScoreFactory()
            for company_id in self.company_ids:
                base_score = factory.create_instance(self.score_name)
                # print(f"New instance created with score_name = {self.score_name}")
                new_score = base_score.get_score(company_id)

                if (
                    new_score
                    and not CompanyScore.objects.is_last_score_value_duplicate(
                        new_score
                    )
                ):
                    new_score.save()
                    self.saved_scores_count += 1
        else:
            print("Non valid data")

    def process_agg_scores(self):

        if self.data_check:
            factory = AggScoreFactory()
            for company_id in self.company_ids:
                agg_score = factory.create_instance(self.score_name)
                # print(f"New instance created with score_name = {self.score_name}")
                new_score = agg_score.get_score(company_id)
                new_score.save()
                self.saved_scores_count += 1
        else:
            print("Non valid data")
