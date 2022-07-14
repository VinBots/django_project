import logging

from django.core.management import BaseCommand
from django.db.models import Sum

from corporates.models import CompanyScore, LatestCompanyScore, ScoreVersion
from ..scoring.scoring import Scoring
from .calc_agg_score import Command as CalcAggScore
from corporates.management.utilities import parse_extract
from .calc_agg_score import calc_agg_score_func


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):
        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")

        calc_score_func(company_id_list)


def calc_score_func(company_id_list):

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

    LatestCompanyScore.objects.filter(company__company_id__in=company_id_list).delete()
    LatestCompanyScore.objects.import_latest_scores(latest_scores)
    calc_agg_score_func(company_id_list)
