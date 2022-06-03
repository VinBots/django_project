import sys, os

from django.conf import settings
from django.core.management import BaseCommand

from corporates.models import Corporate, StockData


sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.finnhub_data import FinnhubData


class Command(BaseCommand):
    def handle(self, *args, **options):

        list_key = Corporate.objects.values_list("company_id", flat=True)
        # list_key = [114]
        requested_fields = [
            "current_c",
            "last_c",
            "pre_pct_chg",
            "last_date",
            "current_date",
            "call_time",
        ]
        stock_data = FinnhubData(requested_fields, list_key)
        scraped_records = stock_data.get_data(date_search="12-31-2021")
        # scraped_records = stock_data.get_data()
        # print(scraped_records)

        filtered_scraped_records = filter(
            lambda v: not StockData.objects.is_last_stock_data_duplicate(v),
            scraped_records,
        )

        count = 0
        for record in filtered_scraped_records:
            record.save()
            count += 1
        print(f"Number of new records saved: {count}")
