import logging

from corporates.models import Corporate, GHGMetrics
from django.core.management import BaseCommand
from corporates.management.ghg_metrics import calculate_ghg_metrics
from corporates.management.utilities import parse_extract


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):
        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")
        calc_ghg_metrics_func(company_id_list)


def calc_ghg_metrics_func(company_id_list):

    GHGMetrics.objects.filter(
        company__company_id__in=company_id_list,
    ).delete()

    years = ["2018", "2019", "2020", "2021", "2022"]
    for year in years:
        count = 0
        for company_id in company_id_list:

            dict = calculate_ghg_metrics(company_id, year)
            if dict:
                ghg_metrics_obj = GHGMetrics(**dict)
            else:
                continue

            if not GHGMetrics.objects.is_last_metrics_duplicate(ghg_metrics_obj):
                ghg_metrics_obj.save()
                count += 1
        logging.info(f"Number of new records for GHG Metrics saved: {count}")
