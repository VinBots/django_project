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

app = DjangoDash(
    name = 'Ex2', 
    cache_arguments = True,
    id = 'company_name',
    cache_timeout_initial_arguments = 1)

app.layout = html.Div(
        [html.Div('HELLO WORLD'),
        dcc.Input(id = 'company_name', type = 'text'),
        html.Div(id = 'another_name', children = 'output'),
        html.Div('HEllo AGAIN!'),
        ])

@app.callback(
    Output(component_id = 'another_name', component_property = 'children'),
    [Input(component_id = 'company_name', component_property = 'value')]
    )
def display_output(value):#, session_state = None, **kwargs):
    """
    if session_state is None:
        return "session state is none"
    csf = session_state.get('demo_state', None)
    if not csf:
        csf = dict(clicks=value)
        session_state['demo_state'] = csf
    else:
        csf['clicks'] = value
    """
    return "call back done " + value