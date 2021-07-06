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


def createscience_based_barchart():

    #Excel file path
    xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

    # Select which columns to extract
    cols_to_use = ['Sector', 'Science-Based Target? (Y/N)']
    
    # Connect to the data source
    df = get_data(
        xlsx_path, 
        'company', 
        cols_to_use,
        )
    
    y0 = df[df['Science-Based Target? (Y/N)'] == 'Y'].groupby('Sector').size()
    y1 = df[df['Science-Based Target? (Y/N)'] == 'N'].groupby('Sector').size()

    trace1 = go.Bar(
        x=list(y0.index),
        y=y0,
        text = y0,
        textposition='auto',
        name = 'Approved',
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
        name = 'No',
        marker = dict(
            color = 'white',
            line = dict(color = 'green',
            width = 2)))
    
    data = [trace1, trace2]
    
    layout = go.Layout (
        barmode = 'stack',
        title = 'SBTi-approved Goals by sector in S&P 100',
        titlefont = dict(family = 'Arial', size = 25),
        xaxis = dict(tickangle = 35, categoryorder = 'category ascending'),
        showlegend = True,
        legend = dict(title = dict (text = "SBTi-approved Goals",
        font = dict(color = 'green'))),
        plot_bgcolor = 'antiquewhite'
        )

    graph = dcc.Graph(
        id='barchart',
        figure = {
            'data': data,
            'layout': layout})
    return graph

app = DjangoDash('sciencebased_dashboard')
sciencebased_barchart = createscience_based_barchart()

# Design the app layout
app.layout = html.Div([
    html.Div([
        html.Div([
                html.H1(children='Science-Based Targets Dashboard'),
                html.H3(children='As validated by SBTi'),
        ], className = 'row'),
        html.Div([
            html.Div([sciencebased_barchart,
                    html.Br(),
                    html.Br(),
                    html.Br()]),
            html.Div([sciencebased_barchart]),])])])

if __name__ == '__main__':
    app.run_server(debug=True)