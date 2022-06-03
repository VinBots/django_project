import sys, os

from django.conf import settings
from django.core.management import BaseCommand

from corporates.models.external_sources.co2_pricing import CO2Pricing

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.co2_data import CO2Data


class Command(BaseCommand):
    def handle(self, *args, **options):
        co2_data = CO2Data()
        scraped_records = co2_data.get_data()

        filtered_scraped_records = filter(
            lambda v: not CO2Pricing.objects.is_last_co2_price_duplicate(v),
            scraped_records,
        )

        count = 0
        for record in filtered_scraped_records:
            record.save()
            count += 1
        print(f"Number of new records saved: {count}")
