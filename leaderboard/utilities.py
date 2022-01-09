from corporates.utilities import get_all_data_from_csv
import os
from pathlib import Path
import json
import pandas as pd
from config import Config as c



BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")

def get_scores_xls(corp_number = None, top_rank=True):
    """
    Fetch companies information according to their score
    By default, fetch all the companies in the database. 
    corp_number specifies the number of companies to return
    if top_rank is set to True, it returns the top ranked companies
    if top_rank is set to False, it returns the bottom ranked companies
    """

    all_data = get_all_data_from_csv(["corp_scores"])["corp_scores"]

    max_rank = all_data[c.SCORES.RANK].max()
    all_data[c.FIELDS.COMPANY_ID] = pd.to_numeric(all_data[c.FIELDS.COMPANY_ID], downcast='integer')
    all_data[c.SCORES.RANK] = pd.to_numeric(all_data[c.SCORES.RANK], downcast='integer')
    all_data[c.SCORES.TRANSPARENCY_RATIO] = pd.to_numeric(all_data[c.SCORES.TRANSPARENCY_RATIO]) * 100
    all_data[c.SCORES.COMMITMENTS_RATIO] = pd.to_numeric(all_data[c.SCORES.COMMITMENTS_RATIO]) * 100
    all_data[c.SCORES.ACTIONS_RATIO] = pd.to_numeric(all_data[c.SCORES.ACTIONS_RATIO]) * 100

    if not corp_number:
        corp_number = max_rank

    if top_rank:
        all_data = all_data.loc[all_data[c.SCORES.RANK]<=corp_number].sort_values(by=[c.SCORES.RANK])
    else:
        all_data = all_data.loc[all_data[c.SCORES.RANK]>max_rank - corp_number].sort_values(by=[c.SCORES.RANK])

    # parsing the DataFrame in json format.
    json_records = all_data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    return data

