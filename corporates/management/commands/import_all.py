from corporates.models import Corporate, GHGQuant, TargetQuant, CDP, Verification
from django.core.management import BaseCommand
from .load_csv import Command as load_csv_cls


from corporates.models import GHGQuant
from .scoring import Scoring
from corporates.utilities import get_last_reporting_year


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        new_instance = load_csv_cls()
        file_path_list = [
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\companies.csv",
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\score_desc.csv",
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\ghg_qual.csv",
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\ghg_quant.csv",
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\targets_quant.csv",
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\net_zero_details.csv",
            r"C:\Users\vince\Documents\django\net0_docs\excel_db\score_details.csv",
        ]
        for file_path in file_path_list:

            dict = {"file_path": file_path}
            new_instance.handle(**dict)
