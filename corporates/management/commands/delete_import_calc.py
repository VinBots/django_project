from django.core.management import BaseCommand

from .load_multiple_csv import Command as load_multiple_csv
from .delete_tables import Command as delete_tables
from .calc_score import Command as calc_score
from .calc_agg_score import Command as calc_agg_score
from ..imports.utilities import (
    create_sp100,
    create_GICS_table,
    remove_empty_ghg_records,
)


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        print("Launch the process")
        delete_tables().handle()
        create_sp100()
        create_GICS_table()
        load_multiple_csv().handle()
        remove_empty_ghg_records()
        calc_score().handle()
        calc_agg_score().handle()
