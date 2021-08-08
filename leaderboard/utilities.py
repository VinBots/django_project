from corporates.utilities import get_data
import os
from pathlib import Path
import json
#import pandas as pd


BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")


def get_scores_xls(corp_rank = 100, top_rank=True):

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
    max_rank = 100
    if top_rank:
        all_data = all_data.loc[all_data['rank']<=corp_rank].sort_values(by=['rank'])
    else:
        all_data = all_data.loc[all_data['rank']>=max_rank - corp_rank].sort_values(by=['rank'])
    # parsing the DataFrame in json format.
    json_records = all_data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    return data

