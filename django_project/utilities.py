
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
from plotly.offline import plot
from corporates.models import Corporate
import random
from pathlib import Path
import json




def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )

def get_random_logos(nb_logos = 5):

    return Corporate.objects.random()



# NOT IN USE
'''
def get_rpt_pct(all_data):
    # query
    cond1 = all_data['2019 Scope 3 '].astype(str).str.isdigit() == True
    cond2 = all_data['2018 Scope 3'].astype(str).str.isdigit() == True
    scope3_report = all_data[cond1 | cond2]['Company Name']
    return len(scope3_report)

def get_perf_pct(all_data):
    # query
    
    return 42
       
def get_net0_pct(all_data):
    # query
    yes = all_data[all_data['Carbon Neutral Goal? (Y/N)'] == 'Y']
    no = all_data[all_data['Carbon Neutral Goal? (Y/N)'] == 'N']
    return int(100 * len(yes) / (len(yes) + len(no)))

def get_sbt_pct(all_data):
    # query
    yes = all_data[all_data['Science-Based Target? (Y/N)'] == 'Y']
    no = all_data[all_data['Science-Based Target? (Y/N)'] == 'N']
    return int(100 * len(yes) / (len(yes) + len(no)))

def get_momentum_pct(all_data):
    # query
    
    return 49
'''

# NOT IN USE
'''
def get_top_stats():

    #Excel file path
    #xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')
    
    BASE_DIR_XL_DB = os.path.join(Path(__file__).parent.parent.parent,'net0_docs','excel_db')
    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')

    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        'company', 
        None,
        )

    rep_pct = get_rpt_pct(all_data)
    perf_pct = get_perf_pct(all_data)
    net0_pct = get_net0_pct(all_data)
    sbt_pct = get_sbt_pct(all_data)
    momentum_pct = get_momentum_pct(all_data)

    return [rep_pct, perf_pct, net0_pct, sbt_pct, momentum_pct]
'''





def get_top10_wo_zero():
 
    # Opening JSON file
    filename = os.path.join ('django_project/static/django_project', 'data', 'top10_wo_net_zero.json')

    with open(filename) as f:
        data = json.load(f)
    
    return data
