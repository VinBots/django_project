import os

from django.core.management import BaseCommand
from .load_csv import Command as load_csv_cls


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        new_instance = load_csv_cls()
        if os.getenv("DJANGO_SETTINGS_MODULE") == "django_project.settings.production":
            print(os.getenv("DJANGO_SETTINGS_MODULE"))
            root_folder = "/home/django/net0_docs/excel_db"
        else:
            root_folder = r"C:\Users\vince\Documents\django\net0_docs\excel_db"

        file_path_list = [
            os.path.join(root_folder, "companies.csv"),
            os.path.join(root_folder, "score_desc.csv"),
            os.path.join(root_folder, "ghg_qual.csv"),
            os.path.join(root_folder, "ghg_quant.csv"),
            os.path.join(root_folder, "targets_quant.csv"),
            os.path.join(root_folder, "net_zero_details.csv"),
            os.path.join(root_folder, "score_details.csv"),
        ]
        for file_path in file_path_list:

            dict = {"file_path": file_path}
            new_instance.handle(**dict)
