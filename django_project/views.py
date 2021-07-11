from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import random
from django_project.utilities import get_top_stats
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

helloWorld = """
<!DOCTYPE html>
<html>
<head>
<title>Net 0 Tracker - Corporate CO2 Emissions</title>
<style>
    body {
        width: 1000px;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background: #AAAAAA;
    }
    div {
      padding: 30px;
      background: #FFFFFF;
      margin: 30px;
      border-radius: 5px;
      border: 1px solid #888888;
    }
    pre {
      padding: 15px;
    }
    code, pre {
      font-size: 16px;
      background: #DDDDDD
    }
</style>
</head>
<body>
  <div>
    <h1>New modification to test the pull functionality</h1>
    <img src="/static/DRL.gif" />
    <h2>Things to do with this script</h2>
    <p>This message is coming to you via a simple Django application that's live on your Droplet! This droplet is all set up with Python, Django, and Postgres. It's also using Gunicorn to run the application on system boot and using nginx to proxy traffic to the application over port 80.</p>
    <h2>Get your code on here</h2>
    <ul>
      <li>SSH into your Droplet. <pre><code>ssh root@{IPADDRESS}</code></pre></li>
      <li>Provide the password that was emailed to you. You can also use an SSH key, if you selected that option during Droplet creation, by <a href='https://www.digitalocean.com/docs/droplets/how-to/add-ssh-keys/'>following these instructions</a>.</li>
      <li>Note the login message, it has important details for connecting to your Postgres database, among other things!</li>
      <li><code>git clone</code> your code onto the droplet. You can try to reuse this project, located in <code>/home/django/django_project</code>, or start fresh in a new location and edit Gunicorn's configuration to point to it at <code>/etc/systemd/system/gunicorn.service</code>. You can also change how nginx is routing traffic by editing <code>/etc/nginx/sites-enabled/django</code></li>
      <ul>
        <li>Note: If you're not using a source control, you can <a href="https://www.digitalocean.com/docs/droplets/how-to/transfer-files/">directly upload the files to your droplet using SFTP</a>.
      </ul>
      <li><code>cd</code> into the directory where your Python  code lives, and install any dependencies. For example, if you have a <code>requirements.txt</code> file, run <code>pip install -r requirements.txt</code>.
      <li>That's it! Whenever you make code changes, reload Gunicorn like so: <pre><code>PID=$(systemctl show --value -p MainPID gunicorn.service) && kill -HUP $PID</code></pre></li>
    </ul>
    <h2>Play in the admin area</h2>
    <p>The standard Django admin area is accessible at <a href="/admin">/admin</a>. The login and password are stored in the <code>DJANGO_USER*</code> values you see when you call  <code>cat /root/.digitalocean_passwords</code> while logged in over SSH.</p>
    <h2>Get production-ready</h2>
    <ul>
      <li><a href="https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04">Set up a non-root user for day-to-day use</a></li>
      <li><a href="https://www.digitalocean.com/docs/networking/firewalls/">Set up a DigitalOcean cloud firewall</a> (they're free).</li>
      <li><a href="https://www.digitalocean.com/docs/networking/dns/quickstart/">Register a custom domain</a></li>
      <li>Have data needs? You can mount a <a href="https://www.digitalocean.com/docs/volumes/">volume</a> (up to 16TB)
        to this server to expand the filesyem, provision a <a href="https://www.digitalocean.com/docs/databases/">database cluster</a> (that runs MySQL, Redis, or PostgreSQL),
        or use a <a href="https://www.digitalocean.com/docs/spaces/">Space</a>, which is an S3-compatible bucket for storing objects.
    </ul>
  </div>
</body>
</html>
"""

def home(request):

  pct_values = get_top_stats()

  angle_deg = [str(pct_values[i] * 1.8) + "deg" for i in range(5)]

  return render (request, "django_project/index.html", {
    "color_key_fig": "#00b118",
    "angle1":angle_deg[0],"value1":str(pct_values[0]),
    "angle2":angle_deg[1],"value2":str(pct_values[1]),
    "angle3":angle_deg[2],"value3":str(pct_values[2]),
    "angle4":angle_deg[3],"value4":str(pct_values[3]),
    "angle5":angle_deg[4], "value5":str(pct_values[4])
    }
      )

def transparency(request):
  return render (request, "django_project/transparency/transparency.html")

def performance(request):
  return render (request, "django_project/performance/performance.html")

def ambition(request):
  return render (request, "django_project/ambition/ambition.html")

def sciencebased(request):
  return render (request, "django_project/sciencebased/sciencebased.html")

def momentum(request):
  return render (request, "django_project/momentum/momentum.html")

def playground(request):
  return render (request, "django_project/playground.html")  

def prototype(request, company_name = "3m - HELLO WORLD"):
  # record 3M dashboard
  record(company_name)
  
  pct_values = get_top_stats()

  angle_deg = [str(pct_values[i] * 1.8) + "deg" for i in range(5)]

  return render (request, "django_project/proto.html", {
    "color_key_fig": "#00b118",
    "angle1":angle_deg[0],"value1":str(pct_values[0]),
    "angle2":angle_deg[1],"value2":str(pct_values[1]),
    "angle3":angle_deg[2],"value3":str(pct_values[2])
    })

 



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

def record(company_name=None):
    
    app = DjangoDash('company_performance_dashboard')
    intensity_bubble = create_performance_bubble()
    ghg_bar = create_ghg_evolution_bar()

    # Design the app layout
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Div(
                    [ghg_bar,
                    intensity_bubble]),
                html.Div([company_name]),])])])

    