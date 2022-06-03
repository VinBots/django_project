import logging

from corporates.models import Corporate, GHGMetrics
from django.core.management import BaseCommand
from corporates.management.ghg_metrics import calculate_ghg_metrics


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        GHGMetrics.objects.all().delete()

        companies = Corporate.objects.all()
        years = ["2018", "2019", "2020"]
        for year in years:
            count = 0
            for company in companies:

                dict = calculate_ghg_metrics(company, year)
                if dict:
                    ghg_metrics_obj = GHGMetrics(**dict)
                else:
                    continue

                if not GHGMetrics.objects.is_last_metrics_duplicate(ghg_metrics_obj):
                    ghg_metrics_obj.save()
                    count += 1
            logging.info(f"Number of new records for GHG Metrics saved: {count}")
