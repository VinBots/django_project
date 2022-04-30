from corporates.models import CompanyScore, Corporate, LatestCompanyScore
from django.core.management import BaseCommand
from django.db.models import Sum
from .scoring import Scoring


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        company_id_list = Corporate.objects.values_list("company_id", flat=True)
        # company_id_list = [66]

        CompanyScore.objects.all().delete()

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

        for score_name in scores_to_test:
            new_score = Scoring(company_ids=company_id_list, score_name=score_name)
            new_score.process_scores()
            print(
                f"{new_score.saved_scores_count} new records were created for score {score_name}"
            )

        results = (
            CompanyScore.objects.values("company__name")
            .annotate(total_score=Sum("score_value"))
            .order_by("-total_score")
        )

        for result in results:
            print(f"{result['company__name']}: {result['total_score']}")

        latest_scores = CompanyScore.objects.get_latest_scores()
        LatestCompanyScore.objects.import_latest_scores(latest_scores)
