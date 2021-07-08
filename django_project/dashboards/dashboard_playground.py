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
import dash_bootstrap_components as dbc

app = DjangoDash(
    "playground_dashboard")

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 3.2,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Temperature"}))

graph = dcc.Graph(
    figure = fig)

app.layout = html.Div(
    [graph]
)

if __name__ == '__main__':
    app.run_server(debug=True)

