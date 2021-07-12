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

a2 = DjangoDash(
    name = 'Ex2',
    id = 'company_name')

a2.layout = html.Div(
    [html.Div('HELLO WORLD'),
    dcc.Input(id = 'company_name', type = 'hidden', value = 'filler text'),
    html.Div(id = 'output_company_name', value = "default"),
    html.Div('HEllo AGAIN!')
    ])

@a2.callback(
    Output('output_company_name', 'children'),
    [Input('company_name', 'value')]
    )
def display_output(value):
    print (value)