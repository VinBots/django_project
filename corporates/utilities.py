import os
from pathlib import Path
from corporates.models import Corporate
import pandas as pd
import os
import math
import json
from config import Config as c

BASE_DIR_XL_DB = os.path.join(c.DATA_FOLDER, c.XLS_FOLDER)
BASE_DIR_LIB = os.path.join(c.DATA_FOLDER, c.LIBRARY_FOLDER)

DIR_TO_CORP_CHARTS_TEMPLATES = "/corporates.html/charts/html_exports/"
DIR_TO_CORP_CHARTS_IMG = "django_project/images/charts/"


def get_path_to_chart(company_id, chart_name):
    path = os.path.join(DIR_TO_CORP_CHARTS_TEMPLATES, chart_name,
                        chart_name + str(company_id) + ".html")
    return path


def get_path_to_img(company_id, chart_name):
    path = os.path.join(DIR_TO_CORP_CHARTS_IMG, chart_name,
                        chart_name + str(company_id) + ".jpeg")

    return path


def check_validity(corp_name):

    cond1 = corp_name is not None
    cond2 = Corporate.objects.filter(name=corp_name).exists()
    conditions = [cond1, cond2]
    return all(conditions)


def get_score_data(company_id, all_data=None):

    score_record_data = all_data[all_data[c.FIELDS.COMPANY_ID] == company_id]
    num_cols = c.SCORES.CATEGORIES + [
        c.SCORES.TOTAL, c.SCORES.RANK
    ]

    score_record_data[num_cols] = score_record_data[num_cols].apply(
        pd.to_numeric)

    score_data = {
        'score': score_record_data[c.SCORES.TOTAL].values[0],
        'rank': score_record_data[c.SCORES.RANK].values[0],
        'transp_ratio': str(round(score_record_data[c.SCORES.TRANSPARENCY_RATIO].values[0] * 100, 1)),
        'transp_angle': score_record_data[c.SCORES.TRANSPARENCY_RATIO].values[0] * 180,
        'comm_ratio': str(round(score_record_data[c.SCORES.COMMITMENTS_RATIO].values[0] * 100, 1)),
        'comm_angle': score_record_data[c.SCORES.COMMITMENTS_RATIO].values[0] * 180,
        'actions_ratio': str(round(score_record_data[c.SCORES.ACTIONS_RATIO].values[0] * 100, 1)),
        'actions_angle': score_record_data[c.SCORES.ACTIONS_RATIO].values[0] * 180,
    }

    return score_data


def get_scores_summary(company_id, all_data=None):

    scores_summary_data = all_data[all_data[c.FIELDS.COMPANY_ID] == company_id]
    score_data_dict = c.SCORES.STRUCTURE
    
    for category in score_data_dict.keys():
        for score in score_data_dict[category]["details"]:
            score["score"] = scores_summary_data[score["field"]].values[0]
        score_data_dict[category]["total"]["score"] = scores_summary_data[score_data_dict[category]["total"]["field"]].values[0]
    
    return score_data_dict


def to_pct(df, field, decimal=1):
    """Converts a field into numeric, multiply by 100 and rounded - used for percentage"""
    df[field] = pd.to_numeric(df[field], errors='coerce') * 100
    df[field] = df[field].round(decimal)
    return df


def get_scores_details(company_id, all_data=None):
    """Returns detailed score data"""
    scores_details_data = all_data[all_data[c.FIELDS.COMPANY_ID] ==
                                   company_id].fillna('NA')
    pct_fields = [
        'rat_6_1',
        'rat_6_2',
        'rat_8_1_meta_1',
        'rat_8_1_meta_2',
        'rat_8_2_meta_1',
        'rat_8_2_meta_2',
        'rat_9_1_meta_1',
        'rat_9_1_meta_2',
        'rat_9_2_meta_1',
        'rat_9_2_meta_2',
    ]
    for field_name in pct_fields:
        scores_details_data = to_pct(scores_details_data, field_name)

    scores_details_data = scores_details_data.fillna('NA')

    return scores_details_data.to_dict(orient='records')[0]


def get_library_data(company_id, all_data=None):
    dict = {}
    fields = ["folder_name", "filename", "desc"]
    cond1 = all_data[c.FIELDS.COMPANY_ID] == company_id
    folders_list = [['sust_report', 'Sustainability Reporting'],
                    ['ghg', 'GHG data'], ['targets', 'Targets reporting'],
                    ['verification', 'Verification']]

    for folder_name, category in folders_list:
        cond2 = all_data['folder_name'] == folder_name
        filter_conditions = cond1 & cond2
        record_data = all_data.loc[filter_conditions].sort_values(
            ['year', 'part'], ascending=[False, True])
        record = record_data[fields].to_dict('records')
        if len(record) > 0:
            dict[category] = record

    return dict


def get_targets(company_id, all_data=None):

    targets_record_data = all_data.loc[
        (all_data[c.FIELDS.COMPANY_ID] == company_id)
        & (all_data['source'].isin(['sbti', 'public', 'cdp']))]
    targets_select_data = targets_record_data[[
        'target_type', 'scope', 'cov_s3', 'reduction_obj', 'base_year',
        'target_year'
    ]]
    targets_select_data[c.TARGETS.REDUCTION_OBJ] = pd.to_numeric(
        targets_select_data[c.TARGETS.REDUCTION_OBJ], errors='coerce') * 100
    data_gross_abs = json.loads(targets_select_data.loc[(targets_select_data[
        c.FIELDS.TARGET_TYPE] == c.TARGETS.TYPE.GROSS_ABSOLUTE)].sort_values(
            by='scope').reset_index().to_json(orient='records'))
    data_net_abs = json.loads(targets_select_data.loc[(targets_select_data[
        c.FIELDS.TARGET_TYPE] == c.TARGETS.TYPE.NET_ABSOLUTE)].sort_values(
            by='scope').reset_index().to_json(orient='records'))
    data_net_zero_policy = json.loads(targets_select_data.loc[(
        targets_select_data[c.FIELDS.TARGET_TYPE] == c.TARGETS.TYPE.NET0_POLICY
    )].sort_values(by='scope').reset_index().to_json(orient='records'))

    targets_dict = {
        'net_zero_policy': data_net_zero_policy,
        'gross_abs': data_gross_abs,
        'net_abs': data_net_abs,
    }

    return targets_dict


def get_ghg(company_id, all_data, reporting_year_data):

    fields = [
        'reporting_year', 'Source', 'ghg_scope_1', 'ghg_loc_scope_2',
        'ghg_mkt_scope_2', 'ghg_scope3_total', 'ghg_total'
    ]
    last_reporting_year = get_last_reporting_year(reporting_year_data,
                                                  company_id)

    cond1 = all_data[c.FIELDS.COMPANY_ID] == company_id
    cond2 = all_data['Source'].isin(['Final'])
    cond3 = all_data['reporting_year'] <= last_reporting_year
    cond4 = all_data['reporting_year'] >= last_reporting_year - 2
    filter_conditions = cond1 & cond2 & cond3 & cond4

    record_data = all_data.loc[filter_conditions].reset_index().sort_values(
        'reporting_year', ascending=False)
    record_data = record_data[fields]  #specific fields only
    dict = record_data.loc[record_data['Source'].isin(
        ['Final'])].reset_index().to_dict()

    for each_dict in dict:
        for key, value in dict[each_dict].items():
            if isinstance(value, float):
                dict[each_dict][key] = int(value)

    data = {
        'final': dict,
    }
    return data

def get_all_data_from_csv(sheet_names):

    pd_dict = {}
    for sheetname in sheet_names:
        csv_path = os.path.join(BASE_DIR_XL_DB, sheetname + '.csv')
        pd_dict[sheetname] = pd.read_csv(csv_path)
    return pd_dict


def get_last_reporting_year(all_data, company_id):

    last_reporting_year = all_data.loc[all_data[
        c.FIELDS.COMPANY_ID] == company_id][['last_reporting_year']].values[0]
    return last_reporting_year


def ghg_format(number):
    if math.isnan(number):
        return "not found"
    else:
        return f'{float(number):,.0f}'


def file_exist(path_name):

    path = os.path.join('/home/django/django_project/django_project/static',
                        path_name)
    return os.path.isfile(path)
