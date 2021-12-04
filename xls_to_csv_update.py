import os
import pandas as pd
from os import listdir
from os.path import isfile, join
import pathlib

sheet_name_list =['ghg_quant', 'corp_scores', 'score_summary', 'targets_quant']

filename = 'sp100.xlsx'

path = pathlib.Path().resolve()

path_to_xls = join(path.parent.parent, 'excel_db', filename)

for sheet_name in sheet_name_list:
    path_to_csv = join(path.parent.parent, 'excel_db', sheet_name + '.csv')
    read_file = pd.read_excel (path_to_xls, sheet_name=sheet_name)
    read_file.to_csv (path_to_csv,
                    index = None,
                    header=True)