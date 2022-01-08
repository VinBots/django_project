import pandas as pd
import os
from corporates.models import Corporate
import json


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