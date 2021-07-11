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

a2 = DjangoDash("Ex2")

a2.layout = html.Div([
    dcc.RadioItems(id="dropdown-one",options=[{'label':i,'value':j} for i,j in [
    ("O2","Oxygen"),("N2","Nitrogen"),("CO2","Carbon Dioxide")]
    ],value="Oxygen"),
    html.Div(children = "hello", id="output-one")
    ])

@a2.callback(
    dash.dependencies.Output('output-one','children'),
    [dash.dependencies.Input('dropdown-one','value')]
    )
def callback_c(*args,**kwargs):
    da = kwargs['dash_app']
    return "Args are [%s] and kwargs are %s" %(",".join(args), kwargs)