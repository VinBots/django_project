import os
from pathlib import Path
from corporates.models import Corporate
import pandas as pd
import os
import math

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
        corp_record_data = corp_record[['gross_total_scope1', 'gross_scope2_calc', 'gross_total_scope3', 'total_scope']]
        corp_record_data = corp_record_data.apply(pd.to_numeric, errors='coerce')
        #merged_df_sector = merged_df_sector.dropna()

        ghg_dict[year] = {
            'scope1':ghg_format(corp_record_data.iloc[0,0]),
            'scope2':ghg_format(corp_record_data.iloc[0,1]),
            'scope3':ghg_format(corp_record_data.iloc[0,2]),
            'total':ghg_format(corp_record_data.iloc[0,3]),
            }
    
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
        'At least 2 years of GHG emissions for scope 1 and 2 are publicly-available',
        'scope 3',
        'verification',
        '',
        'net zero target',
        'intermediate',
        'ambitious',
        'pourquoi pas',
        '',
        'super perf',
        'momentum',
        'remuneration ou offsets',
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
