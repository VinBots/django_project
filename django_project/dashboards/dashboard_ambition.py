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

app = DjangoDash('ambition_dashboard')
ambition_barchart = create_ambition_barchart()

# Design the app layout
app.layout = html.Div([
    html.Div([
        html.Div([
                html.H1(children='Ambition - Key Metrics'),
                html.H3(children=''),
        ], className = 'row'),
        html.Div([
            html.Div([ambition_barchart,
                    html.Br(),
                    html.Br(),
                    html.Br()]),
            html.Div([]),])])])

if __name__ == '__main__':
    app.run_server(debug=True)