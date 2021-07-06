import dash
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_html_components as html
from django_project.utilities import get_data
import os


#Excel file path
xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

# Select which columns to extract
cols_to_use = ['Company Name', 'Sector',
       'Size (2019 Revenue)', '2019 Net Scope 1 + 2 Emissions', '2019 Scope 3 ',
       '2019 Total Scope 1, 2 + 3', '2018 Net Scope 1 + 2 Emissions',
       '2018 Scope 3']

# Connect to the data source
df = get_data(
    xlsx_path, 
    'company', 
    cols_to_use,
    )

df[' index'] = range(1, len(df) + 1)

app = DjangoDash('transparency_dashboard')

PAGE_SIZE = 25

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {"name": i, "id": i} for i in df.columns
    ],
    data=df.to_dict('records'),
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom',
    style_as_list_view=True,
    style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'},),]
        , className = 'col-6 col-12-medium')

@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size")])
def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)