
import pandas as pd
import numpy as np
import os

def get_data(xlsx_path, sheetname, cols_to_use):
    
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )


def get_top_stats():

    #Excel file path
    xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        'company', 
        ['Company Name', 'Science-Based Target? (Y/N)']
        )

    # query
    yes = all_data[all_data['Science-Based Target? (Y/N)'] == 'Y']
    no = all_data[all_data['Science-Based Target? (Y/N)'] == 'N']

    # return a list
    sbt_pct = int(100 * len(yes) / (len(yes) + len(no)))

    return [15, 25, 45, sbt_pct, 47]