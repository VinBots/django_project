from django.core.management import BaseCommand

from corporates.models.grouping import Benchmark
from .import_all import Command as import_all
from .delete_tables import Command as delete_tables
from .calc_score import Command as calc_score
from .calc_agg_score import Command as calc_agg_score
from corporates.models import GHGQuant, CorporateGrouping


def remove_empty_ghg_records():

    for record in GHGQuant.objects.all():
        if record.scope_123_loc == 0 and record.scope_123_mkt == 0:
            record.delete()


def create_sp100():
    # Create a SP100 instance in Benchmark
    record = {
        "name": "SP100",
        "description": "The S&P 100, a sub-set of the S&P 500®, is designed to measure the performance of large-cap companies in the United States and comprises 100 major blue chip companies across multiple industry groups. Individual stock options are listed for each index constituent.",
        "web_URL": "https://www.spglobal.com/spdji/en/indices/equity/sp-100/",
    }
    Benchmark.objects.create(**record)
    record = {
        "name": "SP500",
        "description": "The S&P 500® is widely regarded as the best single gauge of large-cap U.S. equities. According to our Annual Survey of Assets, an estimated USD 13.5 trillion is indexed or benchmarked to the index, with indexed assets comprising approximately USD 5.4 trillion of this total (as of Dec. 31, 2020). The index includes 500 leading companies and covers approximately 80% of available market capitalization.",
        "web_URL": "https://www.spglobal.com/spdji/en/indices/equity/sp-500/",
    }
    Benchmark.objects.create(**record)


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        print("Launch the process")
        delete_tables().handle()
        create_sp100()
        import_all().handle()
        remove_empty_ghg_records()
        calc_score().handle()
        calc_agg_score().handle()
