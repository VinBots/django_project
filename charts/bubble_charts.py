import pandas as pd
import plotly.graph_objs as go
import plotly.offline as offline
import os
import numpy as np
from plotly.offline import plot

def bubble_chart_from_xls(corp_name):

    XLSX_PATH = os.path.join ('../django_project/static/django_project', 'data', 'sp100_ghg.xlsx')
    
    COLS_TO_USE = ['Company Name', 'Sector', 'Size (2019 Revenue)', '2019 Net Scope 1 + 2 Emissions']
    all_data = pd.read_excel(XLSX_PATH, engine = 'openpyxl', usecols = COLS_TO_USE)
    #all_data.to_pickle (os.path.join ('..','data_frame.pickle'))

    all_data["intensity"] = all_data['Size (2019 Revenue)'] /  all_data['2019 Net Scope 1 + 2 Emissions']

    x0 = all_data['2019 Net Scope 1 + 2 Emissions']

    y0 = all_data['Size (2019 Revenue)']

    sector_names = all_data['Sector'].unique()

    sector_data = {sector:all_data.query("Sector == '%s'" %sector) for sector in sector_names}

    upper_left_ann = dict (xref="x domain",
                        yref="paper",
                        x=0.10,
                        y=1.10,
                        text="<b>Corporate Behemoths</b> <br> High Revenue, High Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )
    upper_right_ann = dict (xref="x domain",
                        yref="paper",
                        x=0.90,
                        y=1.10,
                        text="<b>Sustainability Leaders</b> <br> High Revenue, Low Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )
    lower_right_ann = dict (xref="x domain",
                        yref="paper",
                        x=0.90,
                        y=-0.15,
                        text="<b>Small Players</b> <br> Low Revenue, Low Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )
    lower_left_ann = dict (xref="x domain",
                        yref="paper",
                        x=0.10,
                        y=-0.15,
                        text="<b>Worst Offenders</b> <br> Low Revenue, High Emissions",
                        showarrow = False,
                        bgcolor = 'blue',
                        font = {'color':'white'},
                        opacity = 0.5
                        )

    layout = go.Layout (
        title = 'GHG Emissions Intensity',
        title_x = 0.5,
        titlefont = dict(family = 'Arial', size = 25),
        plot_bgcolor = 'antiquewhite',
        xaxis =  dict(autorange = "reversed", type = 'log'),
        yaxis = dict(type = 'log'),
        annotations = [upper_left_ann, upper_right_ann, lower_left_ann, lower_right_ann]
    )

    x_median_x = [x0.min(), x0.max()]
    y_median_x = [y0.median(), y0.median()]
    x_median_y = [x0.median(), x0.median()]
    y_median_y = [y0.min(), y0.max()]

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
                x=1.0,
                xanchor="left",
                y=1.25,
                yanchor="top"
            ),
        ]
    )

    name_fig = "bubble_intensity_{}".format(corp_name)
    fig.write_image("../django_project/static/django_project/images/charts/{}.svg".format(name_fig), scale=3, height = 300)
    plot(fig, filename = '../django_project/static/django_project/images/html_exports/{}.html'.format(name_fig), auto_open=False)

if __name__ == "__main__":
    bubble_chart_from_xls("3m")