from corporates.models import Corporate
from django.core.management import BaseCommand
from corporates.management.scoring.scoring import Scoring


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        company_id_list = Corporate.objects.values_list("company_id", flat=True)
        # company_id_list = [66]
        agg_scores = [
            "Score_total",
            "Score_transparency",
            "Score_commitments",
            "Score_results",
        ]
        base_scores = ["Score_" + str(x) for x in range(1, 11)]
        scores_to_test = base_scores + agg_scores

        for score_name in scores_to_test:
            new_score = Scoring(company_ids=company_id_list, score_name=score_name)
            new_score.process_agg_scores()
            print(
                f"{new_score.saved_scores_count} new records were created for score {score_name}"
            )
