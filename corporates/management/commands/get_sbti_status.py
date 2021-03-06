import os
import sys
from django.conf import settings

from corporates.models import Corporate
from django.core.management import BaseCommand
from corporates.models.external_sources.sbti import SBTI
from corporates.management.utilities import parse_extract

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from providers.sbti_data import SBTiData


class Command(BaseCommand):
    def handle(self, *args, **options):

        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")
        get_sbti_status_func(company_id_list)


def get_sbti_status_func(company_id_list):

    requested_fields = [
        "Near term - Target Status",
        "Near term - Target Classification",
    ]

    sbti = SBTiData(requested_fields=requested_fields, list_key=company_id_list)
    try:
        sbti.download_input_file()
    finally:
        scraped_records = sbti.get_data()
        mapped_companies = scraped_records
        print(f"Number of mapped companies: {len(mapped_companies)}")

        filtered_scraped_records = filter(
            lambda v: not SBTI.objects.is_last_sbti_value_duplicate(v),
            scraped_records,
        )

        count = 0
        for record in filtered_scraped_records:
            record.save()
            count += 1
        print(f"Number of new records saved: {count}")
