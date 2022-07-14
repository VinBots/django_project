import logging
from django.core.management import BaseCommand
from corporates.management.utilities import parse_extract

from .get_tv_financials import get_tv_financials_func
from .get_sbti_status import get_sbti_status_func
from .get_msci_ratings import get_msci_ratings_func
from .get_final_ghg import get_final_ghg_func
from .calc_ghg_metrics import calc_ghg_metrics_func
from .calc_stats import calc_stats_func
from .calc_score import calc_score_func

# from .create_chart import create_chart_func


def update_all(company_id_list):
    sequence_func = [
        get_tv_financials_func,
        get_sbti_status_func,
        get_msci_ratings_func,
        get_final_ghg_func,
        calc_ghg_metrics_func,
        calc_stats_func,
        calc_score_func,
        # create_chart_func,
    ]

    return [func(company_id_list) for func in sequence_func]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):

        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")

        update_all(company_id_list)
