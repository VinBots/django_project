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


def create_ghg_evolution_bar():

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
        titlefont = dict(family = 'Arial'),
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

    return graph

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
    
    upper_left_ann = dict (xref="paper",
                       yref="paper",
                       x=0.0,
                       y=0.90,
                       text="<b>Corporate Behemoths</b> <br> High Revenue, High Emissions",
                       showarrow = False,
                       bgcolor = 'blue',
                       font = {'color':'white'},
                       opacity = 0.5
                      )
    upper_right_ann = dict (xref="paper",
                        yref="paper",
                        x=0.90,
                        y=0.90,
                        text="<b>Sustainability Leaders</b> <br> High Revenue, Low Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )
    lower_right_ann = dict (xref="paper",
                        yref="paper",
                        x=0.90,
                        y=0.10,
                        text="<b>Small Players</b> <br> Low Revenue, Low Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )
    lower_left_ann = dict (xref="paper",
                        yref="paper",
                        x=0.0,
                        y=0.1,
                        text="<b>Worst Offenders</b> <br> Low Revenue, High Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )
                        
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
        title = 'CO2e Emissions Intensity for S&P 100',
        title_x = 0.5,
        titlefont = dict(family = 'Arial'),
        plot_bgcolor = 'antiquewhite',
        xaxis =  dict(autorange = "reversed", type = 'log'),
        yaxis = dict(type = 'log'),
        annotations = [upper_left_ann, upper_right_ann, lower_left_ann, lower_right_ann],
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
    
    num_traces_no_markers = 2
    indexes = list(range(num_traces_no_markers,len(sector_names) + num_traces_no_markers - 1))

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                type = "buttons",
                direction = "left",
                buttons=list([
                    dict(
                        args=["mode", "markers", indexes],
                        label="Hide names",
                        method="restyle"
                    ),
                    dict(
                        args=["mode", "markers+text", indexes],
                        label="Show names",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.3,
                yanchor="top"
            ),
        ]
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="left",
        x=0
    ))

    graph = dcc.Graph(
        id='barchart',
        figure = fig
        )
    return graph

app = DjangoDash('performance_company_dashboard')
#intensity_bubble = create_performance_bubble()
#ghg_bar = create_ghg_evolution_bar()

# Design the app layout
app.layout = html.Div([
    html.P(id="hidden-div-for-slug"),
    html.Div(id='hidden-div-for-slug'),
    html.Div('Hello')])

if __name__ == '__main__':
    app.run_server(debug=True)