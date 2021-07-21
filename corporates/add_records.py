from corporates.models import Corporate
import pandas as pd
import os

def get_name(idx):

    XLSX_PATH = os.path.join ('../django_project/django_project/static/django_project', 'data', 'sp100_data.xlsx')
    
    sheetname = 'companies'
    
    cols = ['company_id', 'company_name']
    
    df = pd.read_excel(
            XLSX_PATH, 
            sheet_name = sheetname,
            engine = 'openpyxl', 
            usecols = cols
            )

    get_corp_name = df[df['company_id']==idx]['company_name']
    if len(get_corp_name) > 0:
        return get_corp_name.iloc[0]

def add_new_records(id_list):

    for idx in id_list:
        corp = Corporate(
            company_id = idx,
            name = get_name(idx),
            filename = 'dummy'
        )
        corp.save()
        print ("executed on idx {} and name {}".format(idx, get_name(idx)))
