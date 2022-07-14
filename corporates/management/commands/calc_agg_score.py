from corporates.models import ScoreVersion
from django.core.management import BaseCommand
from corporates.management.scoring.scoring import Scoring
from corporates.management.utilities import parse_extract


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):
        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")
        calc_agg_score_func(company_id_list)


def calc_agg_score_func(company_id_list):

    active_version = ScoreVersion.objects.get_active_score_version()
    if not active_version:
        print("there is no active score version")
        return

    agg_scores = [
        "Score_total",
        "Score_transparency",
        "Score_commitments",
        "Score_results",
    ]
    base_scores = ["Score_" + str(x) for x in range(1, 11)]
    scores_to_test = base_scores + agg_scores

    for score_name in scores_to_test:
        new_score = Scoring(
            company_ids=company_id_list,
            score_name=score_name,
            version=active_version,
        )
        new_score.process_agg_scores()
        print(
            f"{new_score.saved_scores_count} new records were created for score {score_name}"
        )
