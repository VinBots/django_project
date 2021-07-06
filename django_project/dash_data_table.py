import dash
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_html_components as html
from django_project.utilities import get_data
import dash_core_components as dcc
import os
import plotly.graph_objs as go


#Excel file path
xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

# Select which columns to extract
cols_to_use = ['Sector', '2019 Scope 1 (MeT Co2)', '2019 Scope 2 ', '2019 Scope 3 ']

# Connect to the data source
all_data = get_data(
    xlsx_path, 
    'company', 
    cols_to_use,
    )
all_data[COLS_TO_USE[1]] = pd.to_numeric(all_data[COLS_TO_USE[1]], errors = 'coerce')
all_data[COLS_TO_USE[2]] = pd.to_numeric(all_data[COLS_TO_USE[2]], errors = 'coerce')
all_data[COLS_TO_USE[3]] = pd.to_numeric(all_data[COLS_TO_USE[3]], errors = 'coerce')

total_scope = (all_data[COLS_TO_USE[1]] + all_data[COLS_TO_USE[2]] + all_data[COLS_TO_USE[3]])
all_data['scope1_dist'] = all_data[COLS_TO_USE[1]] / total_scope
all_data['scope2_dist'] = all_data[COLS_TO_USE[2]] / total_scope
all_data['scope3_dist'] = all_data[COLS_TO_USE[3]] / total_scope
all_data['scope_total'] = all_data['scope1_dist'] + all_data['scope2_dist'] + all_data['scope3_dist']

average_scope_by_sector = all_data.groupby('Sector').mean()
x0 = average_scope_by_sector.index
y0=['Scope 1', 'Scope 2', 'Scope 3']
z0 = [average_scope_by_sector['scope1_dist'],
      average_scope_by_sector['scope2_dist'],
      average_scope_by_sector['scope3_dist']]


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
    html.H1(children='Transparency Dashboard'),
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
        'color': 'white'},),
    dcc.Graph(
        id='heatmap',
        figure = {
            'data': [go.Heatmap(
                x = x0,
                y = y0,
                z = z0,
                name = 'hello',
                colorscale = 'amp')],
            'layout': go.layout(
                title = 'GHG Emissions Scope 1, 2, 3 Intensities by Sector',
                titlefont = dict(family = 'Arial', size = 25),
                plot_bgcolor = 'antiquewhite')})] 
                
                ,className = 'col-6 col-12-medium')


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