
import pandas as pd
import numpy as np
import os

def get_data(sheetname, cols_to_use):
    
    XLSX_PATH = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')
    
    return pd.read_excel(
        XLSX_PATH,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )


def get_top_stats():

    # Connect to the data source
    all_data = get_data('company', ['Company Name', 'Science-Based Target? (Y/N)'])

    # query

    # return a list

    return [15, 25, 45, 54, 47]