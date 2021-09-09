import os
from pathlib import Path
from corporates.models import Corporate
import pandas as pd
import os
import math
import json


#BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")
BASE_DIR_XL_DB = os.path.join(Path(__file__).parent.parent.parent,'net0_docs','excel_db')
#DIR_TO_CORP_CHARTS_TEMPLATES = "templates/django_project/corporates/charts/html_exports/"
DIR_TO_CORP_CHARTS_TEMPLATES = "/corporates.html/charts/html_exports/"
DIR_TO_CORP_CHARTS_IMG = "django_project/images/charts/"

def get_path_to_chart(company_id, chart_name):
    path = os.path.join(
        #BASE_DIR,
        DIR_TO_CORP_CHARTS_TEMPLATES,
        chart_name,
        chart_name + str(company_id) + ".html")

    #if os.path.exists(path):
    return path

def get_path_to_img (company_id, chart_name):
    path = os.path.join(
        DIR_TO_CORP_CHARTS_IMG,
        chart_name,
        chart_name + str(company_id) + ".jpeg")

    return path

def check_validity(corp_name):

  cond1 = corp_name is not None
  cond2 = Corporate.objects.filter(name = corp_name).exists()
  conditions = [cond1, cond2]
  return all(conditions)

def get_ghg_xls(company_id):
    ghg_dict={}
    #Excel file path
    #xlsx_path = os.path.join (BASE_DIR, 'static/django_project', 'data', 'sp100_data.xlsx')
    '''
    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')
    year_ghgsheet = [('2017','GHG17'), ('2018','GHG18'), ('2019','GHG19')]

    # Connect to the data source
    for year, ghgsheet in year_ghgsheet:
        all_data = get_data(
            xlsx_path, 
            ghgsheet, 
            None,
            )
        corp_record =  all_data[all_data['company_id']==company_id]
        if corp_record.empty:
            corp_record_data = corp_record[['gross_total_scope1', 'gross_scope2_calc', 'gross_total_scope3', 'total_scope']]
            corp_record_data = corp_record_data.apply(pd.to_numeric, errors='coerce')
            #merged_df_sector = merged_df_sector.dropna()

            ghg_dict[year] = {
                'scope1':ghg_format(corp_record_data.iloc[0,0]),
                'scope2':ghg_format(corp_record_data.iloc[0,1]),
                'scope3':ghg_format(corp_record_data.iloc[0,2]),
                'total':ghg_format(corp_record_data.iloc[0,3]),
                }
    '''
    return ghg_dict

def get_score_data(company_id):
    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')

    all_data = get_data(
        xlsx_path,
        'corp_scores',
        None,
    )
    score_record_data=all_data[all_data['company_id']==company_id]
    score_data = {
        'score': score_record_data.iloc[0,6],
        'rank':score_record_data.iloc[0,7],
        'transp_ratio':str(round(score_record_data.iloc[0,10]*100,1)),
        'transp_angle':score_record_data.iloc[0,10]*180,
        'comm_ratio':str(round(score_record_data.iloc[0,11]*100,1)),
        'comm_angle':score_record_data.iloc[0,11]*180,
        'actions_ratio':str(round(score_record_data.iloc[0,12]*100,1)),
        'actions_angle':score_record_data.iloc[0,12]*180,
    }

    return score_data


def get_scores_summary(company_id):

    principle_ref = [
        '1',
        '2',
        '3',
        '',
        '4',
        '5',
        '6',
        '7',
        '',
        '8',
        '9',
        '10',
        '',
    ]
    principle_statement = [
        'At least 2 years of GHG emissions for scope 1 and 2 are publicly-available and externally-verified',
        'Scope 3 emissions are fully reported and externally-verified',
        'CDP score and interim reporting demonstrate the highest level of transparency',
        '',
        'Net Zero Commitments by 2050 include an intermediate target and cover all the emissions',
        'Net Zero targets demonstrate a high-level of emergency',
        'Emission reduction targets on a forward-looking basis are ambitious',
        'Targets are science-based as validated by SBTi',
        '',
        'Emissions reduction are on-pace vs. cumulative target (performance-to-date)',
        'Recent emissions reduction are on-pace with forward-looking targets (momentum)',
        'Performance can be unambiguously tracked based on a yearly reduction path and a clear stance on offsets contributions',
        '',
    ]
    max_score = [
        '10',
        '10',
        '10',
        '30',
        '10',
        '10',
        '10',
        '10',
        '40',
        '10',
        '10',
        '10',
        '30',
    ]
    comments = [''] * 13

    score_data=[0]*13

    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')
    all_data = get_data(
        xlsx_path,
        'score_summary',
        None,
    )
    scores_summary_data=all_data[all_data['company_id']==company_id]
    for i in range(1, 14):
        score_data[i-1]= scores_summary_data.iloc[0, i]

    score_data_dict = {
        'transparency': {
            'details': [[
                principle_ref[i],
                principle_statement[i],
                score_data[i],
                max_score[i],
                comments[i]] for i in range(0,3)],
            'total': score_data[3],
        },
        'commitments': {
            'details': [[
                principle_ref[i],
                principle_statement[i],
                score_data[i],
                max_score[i],
                comments[i]] for i in range(4,8)],
            'total': score_data[8],
        },
        'actions': {
            'details': [[
                principle_ref[i],
                principle_statement[i],
                score_data[i],
                max_score[i],
                comments[i]] for i in range(9,12)],
            'total': score_data[12],
        },
    }

    return score_data_dict

def get_targets(company_id):

    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')
    cols_to_use = ['company_id', 'target_type','scope', 'cov_s3', 'reduction_obj', 'base_year', 'target_year','source']
    all_data = get_data(
        xlsx_path,
        'targets_quant',
        cols_to_use,
    )
    
    targets_record_data=all_data.loc[(all_data['company_id']==company_id) & (all_data['source'].isin(['sbti','public', 'cdp']))]
    targets_select_data = targets_record_data[['target_type','scope', 'cov_s3', 'reduction_obj', 'base_year', 'target_year']]

    data_gross_abs = json.loads(targets_select_data.loc[(targets_select_data['target_type'] == 'gross_abs')].sort_values(by='scope').reset_index().to_json(orient ='records'))
    data_net_abs = json.loads(targets_select_data.loc[(targets_select_data['target_type'] == 'net_abs')].sort_values(by='scope').reset_index().to_json(orient ='records'))
    data_net_zero_policy = json.loads(targets_select_data.loc[(targets_select_data['target_type'] == 'net_zero_policy')].sort_values(by='scope').reset_index().to_json(orient ='records'))

    targets_dict = {
        'net_zero_policy' : data_net_zero_policy,
        'gross_abs' : data_gross_abs,
        'net_abs' : data_net_abs,
    }

    return targets_dict
    

def get_ghg(company_id = 113, source = 'CDP', last_reporting_year = 2019, fields = ['reporting_year', 'Source', 'ghg_scope_1','ghg_loc_scope_2','ghg_mkt_scope_2','ghg_scope3_total','ghg_total']):
    
    xlsx_path = os.path.join (BASE_DIR_XL_DB, 'sp100.xlsx')
        
    all_data = get_data(
        xlsx_path,
        'ghg_quant',
        None,
    )

    cond1 = all_data['company_id']==company_id
    cond2 = all_data['Source'].isin(['Public', 'CDP', 'Total'])
    cond3 = all_data['reporting_year'] <= last_reporting_year
    cond4 = all_data['reporting_year'] >= last_reporting_year - 2
    filter_conditions = cond1 & cond2 & cond3 & cond4

    record_data=all_data.loc[filter_conditions].reset_index().sort_values('reporting_year', ascending=False)
    record_data = record_data[fields] #specific fields only
    
    return record_data.to_dict()

def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )

def ghg_format(number):
    if math.isnan(number):
        return "not found"
    else:
        return f'{float(number):,.0f}'
