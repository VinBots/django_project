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


app = DjangoDash("playground_dashboard",
                 add_bootstrap_links=True)

app.layout = html.Div(
    [
        dbc.Alert("This is an alert", id="base-alert", color="primary"),
        dbc.Alert(children="Danger", id="danger-alert", color="danger"),
        dbc.Button("Update session state", id="update-button", color="warning"),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)