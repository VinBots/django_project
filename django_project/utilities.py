import pandas as pd
import os
from corporates.models import Corporate
import json
from config import Config as c


def get_random_logos():

    return Corporate.objects.random()


def get_top10_wo_zero():

    # Opening JSON file
    filename = os.path.join('django_project/static/django_project', 'data',
                            'top10_wo_net_zero.json')
    with open(filename) as f:
        data = json.load(f)

    return data


def get_top5_transp_miss_cut():

    # Opening JSON file
    filename = os.path.join('django_project/static/django_project', 'data',
                            'top5_transp_miss_cut.json')
    with open(filename) as f:
        data = json.load(f)

    return data


def get_general_stats(indicators):
    path = os.path.join(c.DATA_FOLDER, c.TOP_STATS_FILE)

    with open(path) as json_file:
        dict = json.load(json_file)

    list_ind = [dict[indicator] for indicator in indicators]
    for ind_dict in list_ind:
        ind_dict['angle'] = str(ind_dict['value'] * 1.8) + "deg"

    return list_ind