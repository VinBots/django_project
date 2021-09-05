from corporates.utilities import get_data
import os
from pathlib import Path
import json
#import pandas as pd


BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")


def get_scores_xls(corp_number = None, top_rank=True):
    """
    Fetch companies information according to their score
    By default, fetch all the companies in the database. 
    corp_number specifies the number of companies to return
    if top_rank is set to True, it returns the top ranked companies
    if top_rank is set to False, it returns the bottom ranked companies
    
    
    """


    #Excel file path
    #xlsx_path = os.path.join (BASE_DIR, 'static/django_project', 'data', 'sp100_data.xlsx')
    BASE_DIR_XL_DB = os.path.join(Path(__file__).parent.parent.parent,'net0_docs','excel_db')
    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')

    sheet_name = "corp_scores"

    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        sheet_name, 
        None,
        )
    max_rank = all_data['rank'].max()
    if not corp_number:
        corp_number = max_rank

    if top_rank:
        all_data = all_data.loc[all_data['rank']<=corp_number].sort_values(by=['rank'])
    else:
        all_data = all_data.loc[all_data['rank']>max_rank - corp_number].sort_values(by=['rank'])

    # parsing the DataFrame in json format.
    json_records = all_data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    return data

