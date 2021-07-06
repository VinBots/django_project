from typing import Dict
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
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Group, Scheme


def create_transparency_datatable():

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
    PAGE_SIZE = 10

    graph = dash_table.DataTable(
                    id='datatable-paging',
                    columns=[{
                        "name": i,
                        "id": i,
                        "type": "numeric",
                        "format": Format(
                            scheme=Scheme.fixed, 
                            precision=0,
                            group=Group.yes,
                            groups=3,
                            group_delimiter='.',
                            decimal_delimiter=',',
                            ) 
                        } for i in df.columns],
                    data=df.to_dict('records'),
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='custom',
                    style_as_list_view=True,
                    style_header={
                        'whitespace': 'normal',
                        'height': 'auto',
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'},
                    style_data={
                        'backgroundColor': 'rgb(200, 200, 200)',
                        'color': 'black'},
                    fill_width=False
                    )

    return graph, df
                        
def create_transparency_heatmap():
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
    all_data[cols_to_use[1]] = pd.to_numeric(all_data[cols_to_use[1]], errors = 'coerce')
    all_data[cols_to_use[2]] = pd.to_numeric(all_data[cols_to_use[2]], errors = 'coerce')
    all_data[cols_to_use[3]] = pd.to_numeric(all_data[cols_to_use[3]], errors = 'coerce')

    total_scope = (all_data[cols_to_use[1]] + all_data[cols_to_use[2]] + all_data[cols_to_use[3]])
    all_data['scope1_dist'] = all_data[cols_to_use[1]] / total_scope
    all_data['scope2_dist'] = all_data[cols_to_use[2]] / total_scope
    all_data['scope3_dist'] = all_data[cols_to_use[3]] / total_scope
    all_data['scope_total'] = all_data['scope1_dist'] + all_data['scope2_dist'] + all_data['scope3_dist']

    average_scope_by_sector = all_data.groupby('Sector').mean()
    x0 = average_scope_by_sector.index
    y0=['Scope 1', 'Scope 2', 'Scope 3']
    z0 = [
        average_scope_by_sector['scope1_dist'],
        average_scope_by_sector['scope2_dist'],
        average_scope_by_sector['scope3_dist']
        ]
    graph = dcc.Graph(
        id='heatmap',
        figure = {
            'data': [go.Heatmap(
                x = x0,
                y = y0,
                z = z0,
                name = 'hello',
                colorscale = 'amp')],
            'layout': go.Layout(
                title = 'GHG Emissions Scope 1, 2, 3 by Sector',
                titlefont = dict(family = 'Arial', size = 25),
                plot_bgcolor = 'antiquewhite')})

    return graph



app = DjangoDash('transparency_dashboard')
transparency_datatable, df = create_transparency_datatable()
transparency_heatmap = create_transparency_heatmap()

# Design the app layout
app.layout = html.Div([
    html.Div([
        html.Div([
                html.H1(children='Transparency Dashboard'),
                html.H3(children='Scope 1,2 and 3 Emissions'),
        ], className = 'row'),
        html.Div([
            html.Div([transparency_heatmap,
                    html.Br(),
                    html.Br(),
                    html.Br()]),
            html.Div([transparency_datatable]),])])])

# Callbacks
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