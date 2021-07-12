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
    id = 'company_name')

app.layout = html.Div(
        [html.Div('HELLO WORLD'),
        dcc.Input(id = 'company_name', type='text' , value = 'xx'),
        html.Div(id = 'another_name'),
        html.Div('HEllo AGAIN!'),
        ])

@app.callback(
    Output(component_id = 'another_name', component_property = 'children'),
    [Input(component_id = 'company_name', component_property = 'value')]
    )
def display_output(value, session_state = None, **kwargs):
    if session_state is None:
        raise NotImplementedError ("Cannot handle a missing session state")
    csf = session_state.get('demo_state', None)
    if not csf:
        csf = dict(clicks=value)
        session_state['demo_state'] = csf
    else:
        csf['clicks'] = value
    return "call back done " + value

"""
app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='company_name', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
"""