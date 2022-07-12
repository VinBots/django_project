from corporates.models import CompanyScore, Corporate, LatestCompanyScore, ScoreVersion
from django.core.management import BaseCommand
from django.db.models import Sum

from ..scoring.scoring import Scoring
import logging
from .calc_agg_score import Command as CalcAggScore


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        company_id_list = Corporate.objects.values_list("company_id", flat=True)
        # company_id_list = [14]
        # CompanyScore.objects.all().delete()

        active_version = ScoreVersion.objects.get_active_score_version()
        if not active_version:
            print("there is no active score version")
            return

        score_names = [
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

        for score_name in score_names:
            new_score = Scoring(
                company_ids=company_id_list,
                score_name=score_name,
                version=active_version,
            )
            new_score.process_scores()
            logging.info(
                f"{new_score.saved_scores_count} new records were created for score {score_name}"
            )

        latest_scores = CompanyScore.objects.get_latest_scores(version=active_version)

        LatestCompanyScore.objects.all().delete()
        LatestCompanyScore.objects.import_latest_scores(latest_scores)
        CalcAggScore().handle()
