import os
from pathlib import Path
from corporates.models import Corporate
import pandas as pd
import os


BASE_DIR = os.path.join(Path(__file__).parent.parent, "django_project")
DIR_TO_CORP_CHARTS_TEMPLATES = "templates/django_project/corporates/charts/html_exports/"

def get_path_to_bubble(filename):
    path = os.path.join(
        BASE_DIR,
        DIR_TO_CORP_CHARTS_TEMPLATES) + "bubble_intensity_"+ filename + ".html"

    if os.path.exists(path):
        return path

def check_validity(corp_name):

  cond1 = corp_name is not None
  cond2 = Corporate.objects.filter(name = corp_name).exists()
  conditions = [cond1, cond2]
  return all(conditions)

def get_ghg_xls(company_id):
    
    #Excel file path
    xlsx_path = os.path.join (BASE_DIR, 'static/django_project', 'data', 'sp100_data.xlsx')

    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        'GHG19', 
        None,
        )
    corp_record =  all_data[all_data['company_id']==company_id]
    corp_record_data = corp_record[['gross_total_scope1', 'gross_loc_scope2', 'gross_total_scope_3']]
    ghg_dict = {
        '2017':{'scope1':str(corp_record_data.iloc[0,0]), 'scope2':str(corp_record_data.iloc[0,1]), 'scope3':str(corp_record_data.iloc[0,2])},
        '2018':{'scope1':str(corp_record_data.iloc[0,0]), 'scope2':str(corp_record_data.iloc[0,1]), 'scope3':str(corp_record_data.iloc[0,2])},
        '2019':{'scope1':str(corp_record_data.iloc[0,0]), 'scope2':str(corp_record_data.iloc[0,1]), 'scope3':f'{corp_record_data.iloc[0,2]:,}'},
        }
    
    return ghg_dict


def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )
