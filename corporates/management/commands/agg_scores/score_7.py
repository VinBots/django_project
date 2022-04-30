from .abs_agg_score import AbsAggScore


class Score_7(AbsAggScore):
    """
    Aggregate all the base scores Score_x_1, Score_x_2, Score_x_3
    """

    def get_rating(self):

        return self.filter_sum(score_number=7)
