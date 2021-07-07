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


def create_ambition_barchart():

    #Excel file path
    xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

    # Select which columns to extract
    cols_to_use = ['Sector', 'Carbon Neutral Goal? (Y/N)']
    
    # Connect to the data source
    df = get_data(
        xlsx_path, 
        'company', 
        cols_to_use,
        )
    
    y0 = df[df['Carbon Neutral Goal? (Y/N)'] == 'Y'].groupby('Sector').size()
    y1 = df[df['Carbon Neutral Goal? (Y/N)'] == 'N'].groupby('Sector').size()

    trace1 = go.Bar(
        x=list(y0.index),
        y=y0,
        text = y0,
        textposition='auto',
        name = 'Stated',
        marker = dict(
            color = 'green',
            line = dict(
                color = 'green',
                width = 2)))
    
    trace2 = go.Bar(
        x=list(y1.index),
        y=y1,
        text = y1,
        textposition='auto',
        name = 'Not Stated',
        marker = dict(
            color = 'white',
            line = dict(color = 'green',
            width = 2)))
    
    data = [trace1, trace2]
    
    layout = go.Layout (
        barmode = 'stack',
        title = 'Net Zero Goals by Sector in S&P 100',
        titlefont = dict(family = 'Arial'),
        xaxis = dict(tickangle = 35, categoryorder = 'category ascending'),
        showlegend = True,
        legend = dict(title = dict (text = "Net Zero Goals",
        font = dict(color = 'green'))),
        plot_bgcolor = 'antiquewhite'
        )

    graph = dcc.Graph(
        id='barchart',
        figure = {
            'data': data,
            'layout': layout})
    return graph

def create_ambition_table():
    
    #Excel file path
    xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

    # Select which columns to extract
    cols_to_use = ['Company Name', 'Sector', 'Carbon Neutral Goal? (Y/N)']
    
    header_text = ['Company', 'Sector', 'Net 0 Goal Stated']
    # Connect to the data source
    df = get_data(
        xlsx_path, 
        'company', 
        cols_to_use,
        )
    df = df[df['Carbon Neutral Goal? (Y/N)']=='N']
    df = df[['Company Name', 'Sector']]

    PAGE_SIZE = 10
    
    data_table_cols=[{
        "name": i,
        "id": i,
        "type": "numeric"
        } for i in df.columns]
    
    for i in range(len(header_text)):
        data_table_cols[i]["name"] = header_text[i]
    
    graph = dash_table.DataTable(
                    id='datatable-paging',
                    columns = data_table_cols,
                    data=df.to_dict('records'),
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='custom',
                    style_as_list_view=False,
                    style_cell = {
                        'font-family': 'Lato',
                        'whitespace': 'normal',
                        'height': 'auto',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'
                        },
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                        },
                    style_data={
                        'backgroundColor': 'rgb(200, 200, 200)',
                        'color': 'black'},
                    fill_width=False
                    )
    return graph, df

app = DjangoDash('ambition_dashboard')
ambition_barchart = create_ambition_barchart()
ambition_table, df = create_ambition_table()

# Design the app layout
app.layout = html.Div([
    html.Div([
        html.Div([
                html.H1(children='Ambition - Key Metrics'),
                html.H3(children=''),
        ], className = 'row'),
        html.Div([
            html.Div([
                html.H1(children='Companies without publicly-stated net zero goal'),
                html.H3(children=''),
        ], className = 'row'),
            html.Div([ambition_barchart,
                    html.Br(),
                    html.Br(),
                    html.Br()]),
            html.Div([ambition_table]),])])])

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