import os
from pathlib import Path
import json
import pandas as pd
from corporates.utilities import get_all_data_from_csv


BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")

def get_market_stats(corp_number = None, top_rank=True):
    """
    Fetch companies market statistics information
    By default, fetch all the companies in the database. 
    corp_number specifies the number of companies to return
    if top_rank is set to True, it returns the top ranked companies
    if top_rank is set to False, it returns the bottom ranked companies
    
    
    """
    # Connect to the data source
    all_data = get_all_data_from_csv(["market_stats"])["market_stats"]
    
    """ 
    max_rank = all_data['rank'].max()
    all_data['company_id'] = pd.to_numeric(all_data['company_id'], downcast='integer')
    all_data['rank'] = pd.to_numeric(all_data['rank'], downcast='integer')
    all_data['transp_ratio'] = pd.to_numeric(all_data['transp_ratio']) * 100
    all_data['comm_ratio'] = pd.to_numeric(all_data['comm_ratio']) * 100
    all_data['actions_ratio'] = pd.to_numeric(all_data['actions_ratio']) * 100 """
    """     
    
    if not corp_number:
        corp_number = max_rank

    if top_rank:
        all_data = all_data.loc[all_data['rank']<=corp_number].sort_values(by=['rank'])
    else:
        all_data = all_data.loc[all_data['rank']>max_rank - corp_number].sort_values(by=['rank']) 
    
    """
    # parsing the DataFrame in json format.
    json_records = all_data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    return data

