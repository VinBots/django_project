import os
import sys

from django.conf import settings
from django.core.management import BaseCommand

from corporates.models import Tradingview
from corporates.management.utilities import parse_extract

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.tradingview_data import TradingviewData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):

        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")
        get_tv_financials_func(company_id_list)


def get_tv_financials_func(company_id_list):

    requested_fields = ["Revenue", "EBITDA"]
    tv = TradingviewData(requested_fields=requested_fields, list_key=company_id_list)
    scraped_records = tv.get_data()
    filtered_scraped_records = filter(
        lambda v: not Tradingview.objects.is_last_tv_value_duplicate(v),
        scraped_records,
    )

    count = 0
    for record in filtered_scraped_records:
        record.save()
        count += 1
    print(f"Number of new records saved: {count}")
