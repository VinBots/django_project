import logging

from corporates.models.metrics import Stats, CalcMetrics
from corporates.models.corp import Corporate
from corporates.management.total_carbon_emissions import TotalCarbonEmissions
from corporates.models.choices import Options
from django.core.management import BaseCommand

methods = Options.CO2_ESTIMATES_METHODS


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        # GHGMetrics.objects.all().delete()
        # CalcMetrics.objects.all().delete()
        count = 0
        # years = ["2018", "2019", "2020", "2021"]
        # for year in years:
        #     stats_list = Stats.objects.calc_sector_intensity(year)
        #     for stat in stats_list:
        #         if not Stats.objects.is_last_stats_duplicate(stat):
        #             stat.save()
        #             count += 1
        #     logging.info(
        #         f"Number of new records for Sector Stats (year: {year}) saved: {count}"
        #     )

        #     stat = Stats.objects.calc_average_intensity(year)
        #     if not Stats.objects.is_last_stats_duplicate(stat):
        #         stat.save()
        #         count += 1
        #     logging.info(
        #         f"Number of new records for Average Intensity (year: {year}) saved: {count} - stat value = {stat.value}"
        #     )

        company_list = Corporate.objects.all()
        # company_list = Corporate.objects.filter(company_id__in=[1, 2, 3, 430])
        years = ["2018", "2019", "2020", "2021"]
        for year in years:
            for company in company_list:
                carbon_emissions = TotalCarbonEmissions(company, year)
                carbon_emissions.calculate()
                carbon_emissions.save()
