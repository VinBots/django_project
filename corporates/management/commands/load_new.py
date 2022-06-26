import os

from django.conf import settings
from django.core.management import BaseCommand
from .load_single_csv import Command as load_csv_cls


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        new_instance = load_csv_cls()

        root_folder = os.path.join(settings.EXCEL_DB_FOLDER, "csv_extracts")

        dict = {"file_path": os.path.join(root_folder, "new_input.csv")}
        new_instance.handle(**dict)
