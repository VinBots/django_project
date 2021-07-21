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

def add_records(id_list):

    for idx in id_list:
        corp = Corporate.create(
            company_id = idx,
            name = get_name(idx),
            filename = 'dummy'
        )
        print ("executed on idx {} and name {}".format(idx, get_name(idx)))


if __name__ == "__main__":
    id_list = list(range(90, 92, 1))
    print (add_records(id_list))