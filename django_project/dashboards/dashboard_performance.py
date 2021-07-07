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


def create_performance_bubble():

    #Excel file path
    xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')

    # Select which columns to extract
    cols_to_use = [
        'Company Name',
        'Sector', 
        'Size (2019 Revenue)', 
        '2019 Net Scope 1 + 2 Emissions']
    
    # Connect to the data source
    df = get_data(
        xlsx_path, 
        'company', 
        cols_to_use,
        )
    df["intensity"] = df['Size (2019 Revenue)'] /  df['2019 Net Scope 1 + 2 Emissions']

    x0 = df['2019 Net Scope 1 + 2 Emissions']
    y0 = df['Size (2019 Revenue)']

    x_median_x = [x0.min(), x0.max()]
    y_median_x = [y0.median(), y0.median()]
    x_median_y = [x0.median(), x0.median()]
    y_median_y = [y0.min(), y0.max()]

    sector_names = df['Sector'].unique()
    sector_data = {
        sector:df.query("Sector == '%s'" %sector) for sector in sector_names
        }
    trace1 = go.Scatter(x=x_median_y, 
                    y=y_median_y, 
                    showlegend = False, 
                    name='Median y',
                    mode = "lines",
                    line = dict(color='gray', 
                                width=2, 
                                dash='dash'))

    trace2 = go.Scatter(x=x_median_x, 
                            y=y_median_x, 
                            showlegend = False, 
                            name='Median x', 
                            mode = "lines",
                            line = {'color':'gray', 
                                    'width':2, 
                                    'dash':'dash'}
                            )
    
    data = [trace1, trace2]
    
    layout = go.Layout (
        title = 'GHG Emissions Intensity',
        title_x = 0.5,
        titlefont = dict(family = 'Arial', size = 25),
        plot_bgcolor = 'antiquewhite',
        xaxis =  dict(autorange = "reversed", type = 'log'),
        yaxis = dict(type = 'log'),
        height = 700,
        )

    fig = go.Figure(data = [trace1, trace2], 
                layout = layout)
    
    for sector_name, sector in sector_data.items():
        fig.add_trace(go.Scatter(
            x=sector['2019 Net Scope 1 + 2 Emissions'], y=sector['Size (2019 Revenue)'],
            name=sector_name, 
            text=sector['Company Name'],
            mode = 'markers',
            marker_size=10,
            textposition='top center'
            ))

    graph = dcc.Graph(
        id='barchart',
        figure = fig
        )
    
    return graph

app = DjangoDash('performance_dashboard')
performance_barchart = create_performance_bubble()

# Design the app layout
app.layout = html.Div([
    html.Div([
        html.Div([
                html.H1(children='Net Zero Targets Dashboard'),
                html.H3(children='As stated publicly'),
        ], className = 'row'),
        html.Div([
            html.Div([performance_barchart,
                    html.Br(),
                    html.Br(),
                    html.Br()]),
            html.Div([]),])])])

if __name__ == '__main__':
    app.run_server(debug=True)