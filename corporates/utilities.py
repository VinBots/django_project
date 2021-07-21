import os
from pathlib import Path
from corporates.models import Corporate
import pandas as pd
import os


BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")
DIR_TO_CORP_CHARTS_TEMPLATES = "templates/django_project/corporates/charts/html_exports/"

def get_path_to_bubble(company_id):
    path = os.path.join(
        BASE_DIR,
        DIR_TO_CORP_CHARTS_TEMPLATES) + "intensity_idx"+ str(company_id) + ".html"

    if os.path.exists(path):
        return path

def check_validity(corp_name):

  cond1 = corp_name is not None
  cond2 = Corporate.objects.filter(name = corp_name).exists()
  conditions = [cond1, cond2]
  return all(conditions)

def get_ghg_xls(company_id):
    ghg_dict={}
    #Excel file path
    xlsx_path = os.path.join (BASE_DIR, 'static/django_project', 'data', 'sp100_data.xlsx')
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
        ghg_dict[year] = {
            'scope1':ghg_format(corp_record_data.iloc[0,0]),
            'scope2':ghg_format(corp_record_data.iloc[0,1]),
            'scope3':ghg_format(corp_record_data.iloc[0,2]),
            'total':ghg_format(corp_record_data.iloc[0,3]),
            }
    
    return ghg_dict


def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )

def ghg_format(number):
    return f'{float(number):,.0f}'
