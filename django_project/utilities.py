import pandas as pd
#import numpy as np
import os
#import plotly.graph_objs as go
#from plotly.offline import plot
from corporates.models import Corporate
#import random
#from pathlib import Path
import json

'''
def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )
'''

def get_random_logos():

    return Corporate.objects.random()

def get_top10_wo_zero():
 
    # Opening JSON file
    filename = os.path.join ('django_project/static/django_project', 'data', 'top10_wo_net_zero.json')

    with open(filename) as f:
        data = json.load(f)
    
    return data

def get_top5_transp_miss_cut():
 
    # Opening JSON file
    filename = os.path.join ('django_project/static/django_project', 'data', 'top5_transp_miss_cut.json')

    with open(filename) as f:
        data = json.load(f)
    
    return data