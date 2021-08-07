from corporates.utilities import get_data
import os
from pathlib import Path
#import pandas as pd


BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")


def get_scores_xls(top_rank = 100):

    scores_dict={}
    #Excel file path
    xlsx_path = os.path.join (BASE_DIR, 'static/django_project', 'data', 'sp100_data.xlsx')
    sheet_name = "corp_scores"

    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        sheet_name, 
        None,
        )
    scores_dict = all_data.to_dict("series")
    
    return scores_dict