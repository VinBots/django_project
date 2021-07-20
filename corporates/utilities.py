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

def get_ghg_xls(corp_name):
    
    #Excel file path
    xlsx_path = os.path.join (BASE_DIR, 'static/django_project', 'data', 'sp100_data.xlsx')

    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        'GHG19', 
        None,
        )
    
    company_id = 4
    corp_record =  all_data[all_data['company_id']==company_id]
    corp_record_scope1 = corp_record['gross_total_scope1'].iloc[0]
    
    ghg_dict = {
        '2017':{'scope1':"20", 'scope2':"10", 'scope3':"20",'total':"50"},
        '2018':{'scope1':"5", 'scope2':"15", 'scope3':"25",'total':"45"},
        '2019':{'scope1':str(corp_record_scope1), 'scope2':"19", 'scope3':"29",'total':"57"}}
    
    return ghg_dict


def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )
