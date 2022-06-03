import os, csv

from django.conf import settings

from corporates.models.grouping import Benchmark, GICS
from corporates.models import GHGQuant


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


def create_GICS_table():

    file_path = os.path.join(settings.EXCEL_DB_FOLDER, "csv_extracts", "GICS.csv")

    with open(file_path, "r", encoding="utf8") as csv_file:
        data = csv.DictReader(csv_file)
        for row in data:
            record = {
                "sub_industry_name": row["sub_industry_name"],
                "industry_name": row["industry_name"],
                "industry_group_name": row["industry_group_name"],
                "sector_name": row["sector_name"],
            }
            GICS.objects.create(**record)
