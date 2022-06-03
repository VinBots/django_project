import os
import sys
from django.conf import settings

from corporates.models import Corporate, Tradingview
from django.core.management import BaseCommand

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.tradingview_data import TradingviewData


class Command(BaseCommand):
    def handle(self, *args, **options):
        company_id_list = Corporate.objects.values_list("company_id", flat=True)
        requested_fields = ["Revenue", "EBITDA"]
        tv = TradingviewData(
            requested_fields=requested_fields, list_key=company_id_list
        )
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
