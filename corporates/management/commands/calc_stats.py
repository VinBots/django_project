import logging

from django.core.management import BaseCommand

from corporates.models.metrics import Stats, CalcMetrics
from corporates.models.corp import Corporate
from corporates.management.total_carbon_emissions import TotalCarbonEmissions
from corporates.models.choices import Options
from corporates.management.utilities import parse_extract

methods = Options.CO2_ESTIMATES_METHODS


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):
        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")
        calc_stats_func(company_id_list)


def calc_stats_func(company_id_list):

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

    years = ["2018", "2019", "2020", "2021", "2022"]
    for year in years:
        for company_id in company_id_list:
            carbon_emissions = TotalCarbonEmissions(company_id, year)
            carbon_emissions.calculate()
            carbon_emissions.save()
