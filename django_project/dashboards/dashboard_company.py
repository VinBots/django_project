
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


app = DjangoDash('company_performance_dashboard')
app.layout = html.Div([
        html.Div([
            html.Div([
                html.Div(
                    ["gg",
                    "hh"]),
                html.Div(["company_name"]),])])])