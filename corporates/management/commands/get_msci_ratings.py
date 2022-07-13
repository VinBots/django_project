import os
import sys
from django.conf import settings

from corporates.models import Corporate, MSCI
from django.core.management import BaseCommand
from corporates.models.external_sources.msci import MSCI

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.msci_data import MSCIData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):

        company_id = options.get("company_id", None)
        if company_id:
            company_id_list = [company_id]
        else:
            company_id_list = Corporate.objects.values_list("company_id", flat=True)

        requested_fields = [
            "itr",
            "decarb_target",
            "decarb_target_in_calc",
            "target_year",
            "comprehensiveness",
            "ambition",
            "target_data_date",
            "rating",
        ]

        msci = MSCIData(requested_fields=requested_fields, list_key=company_id_list)
        scraped_records = msci.get_data()

        filtered_scraped_records = filter(
            lambda v: not MSCI.objects.is_last_msci_value_duplicate(v),
            scraped_records,
        )

        count = 0
        for record in filtered_scraped_records:
            record.save()
            count += 1
        print(f"Number of new records saved: {count}")
