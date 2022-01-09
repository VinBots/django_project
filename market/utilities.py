import os
from pathlib import Path
import json
import pandas as pd
from corporates.utilities import get_all_data_from_csv
from config import Config as c


def get_market_stats():
    """
    Fetch companies market statistics information
    By default, fetch all the companies in the database. 
    corp_number specifies the number of companies to return
    if top_rank is set to True, it returns the top ranked companies
    if top_rank is set to False, it returns the bottom ranked companies
    """

    # Connect to the data source
    all_data = get_all_data_from_csv(["market_stats"])["market_stats"]
    all_data[c.FIELDS.COMPANY_ID] = pd.to_numeric(all_data[c.FIELDS.COMPANY_ID], downcast='integer')

    # parsing the DataFrame in json format.
    json_records = all_data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    return data

def get_meta_data():
    path = '/home/django/scripts/data/meta_data.json'
    with open(path) as json_file:
        return json.load(json_file)
