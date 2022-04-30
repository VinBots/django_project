from .abs_agg_score import AbsAggScore


class NullScore(AbsAggScore):
    def get_rating(self, score_value):
        pass

    def map_rating_to_score(self, rating):
        pass

    def get_score(self, company_id):
        print("overriden")
