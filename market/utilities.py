import os
import json
import pandas as pd

from django_project.settings.common import SERVER_BASE_DIR

from corporates.utilities import get_all_data_from_csv
from corporates.models import LatestCompanyScore


def get_market_stats():
    """
    Fetch companies market statistics information
    """

    # Connect to the data source
    all_data = get_all_data_from_csv(["market_stats"])["market_stats"]
    all_data["company_id"] = pd.to_numeric(all_data["company_id"], downcast="integer")

    # parsing the DataFrame in json format.
    json_records = all_data.reset_index().to_json(orient="records")
    data = []
    data = json.loads(json_records)
    for company_dict in data:
        company_dict.update(
            {
                "score_db": LatestCompanyScore.objects.get_latest_company_score_value(
                    company_id=company_dict["company_id"], score_name="Score_total"
                ).values_list("latest_score_value", flat=True)[0]
            }
        )
    return data


def get_meta_data():
    path = os.path.join(SERVER_BASE_DIR, "scripts/data/meta_data.json")
    with open(path) as json_file:
        return json.load(json_file)
