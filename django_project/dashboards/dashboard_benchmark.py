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

def get_layout():
    return html.Div(
        [html.Div('HELLO WORLD'),
        dcc.RadioItems(id="companyname", options = [
            {'label': 'O2', "value": 'Oxygen'},
            {'label': 'corp', "value": "OLD VALUE"}], value = "Oxygen"),
        html.Div(id = 'another_name', children = 'x'),
        html.Div('HEllo AGAIN!'),
        ])

"""
DashApp = apps.get_model("django_plotly_dash","DashApp")
StatelessApp = apps.get_model("django_plotly_dash","StatelessApp")

sa1 = StatelessApp(app_name="SimpleExample",
                    slug="simple-example")

sa1.save()

da1 = DashApp(stateless_app=sa1,
                instance_name="SimpleExample-1",
                slug="simpleexample-1",
                base_state='{"dropdown-color":{"value":"blue"},"dropdown-size":{"value":"small"}}')

da1.save()
"""
app = DjangoDash(
    name = "Ex2",
    id = "companyname",
    serve_locally = False
    )

app.layout = get_layout()


dis = DjangoDash("DjangoSessionState",
                 add_bootstrap_links=True)

dis.layout = html.Div(
    [
        html.Div(children="Danger", id="danger-alert"),
        dcc.Input(id="update-button", value="warning"),
    ]
)

@dis.callback(
    dash.dependencies.Output("danger-alert", 'children'),
    [dash.dependencies.Input('update-button', 'value'),]
    )
def session_demo_danger_callback(n_clicks, session_state=None, **kwargs):
    if session_state is None:
        raise NotImplementedError("Cannot handle a missing session state")
    csf = session_state.get('bootstrap_demo_state', None)
    if not csf:
        csf = dict(clicks=0)
        session_state['bootstrap_demo_state'] = csf
    else:
        csf['clicks'] = n_clicks
    return "Button has been clicked %s times since the page was rendered" %n_clicks

@app.callback(
    Output(component_id = 'another_name', component_property = 'children'),
    [Input(component_id = 'companyname', component_property = 'value')]
    )
def display_output(x, *args, **kwargs):
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
    return "call back done input = {} args = {} kwargs = {}".format(x, args, kwargs)

