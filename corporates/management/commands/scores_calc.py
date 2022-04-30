from corporates.management.commands.scoring import Scoring
from corporates.models import Verification, CompanyScore, Corporate, Score, TargetQuant
from django.core.management import BaseCommand
from corporates.models import GHGQuant


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        score_calc()


def score_calc():
    company_id = 45
    test_1_1(company_id)


def test_1_1(company_id):

    score_name = "Score_1_1"
    company = Corporate.objects.get(company_id=company_id)
    # Verification.objects.create(company=company, scope12_reporting_2_years="yes")
    score_value = get_score([company_id], score_name)
    assert score_value.score_value == 5.0
    assert score_value.rating_value == "yes"


def get_score(company_id, score_name):

    new_scoring = Scoring(company_ids=company_id, score_name=score_name)
    score_value = new_scoring.process_scores()
    return score_value


"""
    scores_to_test = [
        "Score_1_1",
        "Score_1_2",
        "Score_2_1",
        "Score_2_2",
        "Score_3_1",
        "Score_4_1",
        "Score_4_2",
        "Score_4_3",
        "Score_5_1",
        "Score_5_2",
        "Score_6_1",
        "Score_6_2",
        "Score_7_1",
        "Score_8_1",
        "Score_8_2",
        "Score_9_1",
        "Score_9_2",
        "Score_10_1",
    ]
"""
