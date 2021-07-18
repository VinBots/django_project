
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
from plotly.offline import plot


def get_data(xlsx_path, sheetname, cols_to_use):
    
    return pd.read_excel(
        xlsx_path,
        sheet_name=sheetname, 
        engine = 'openpyxl',
        usecols=cols_to_use
        )



def get_rpt_pct(all_data):
    # query
    cond1 = all_data['2019 Scope 3 '].astype(str).str.isdigit() == True
    cond2 = all_data['2018 Scope 3'].astype(str).str.isdigit() == True
    scope3_report = all_data[cond1 | cond2]['Company Name']
    return len(scope3_report)

def get_perf_pct(all_data):
    # query
    
    return 48
       
def get_net0_pct(all_data):
    # query
    yes = all_data[all_data['Carbon Neutral Goal? (Y/N)'] == 'Y']
    no = all_data[all_data['Carbon Neutral Goal? (Y/N)'] == 'N']
    return int(100 * len(yes) / (len(yes) + len(no)))

def get_sbt_pct(all_data):
    # query
    yes = all_data[all_data['Science-Based Target? (Y/N)'] == 'Y']
    no = all_data[all_data['Science-Based Target? (Y/N)'] == 'N']
    return int(100 * len(yes) / (len(yes) + len(no)))

def get_momentum_pct(all_data):
    # query
    
    return 24



def get_top_stats():

    #Excel file path
    xlsx_path = os.path.join ('django_project/static/django_project', 'data', 'sp100_data.xlsx')
    
    # Connect to the data source
    all_data = get_data(
        xlsx_path, 
        'company', 
        None,
        )

    rep_pct = get_rpt_pct(all_data)
    perf_pct = get_perf_pct(all_data)
    net0_pct = get_net0_pct(all_data)
    sbt_pct = get_sbt_pct(all_data)
    momentum_pct = get_momentum_pct(all_data)

    return [rep_pct, perf_pct, net0_pct, sbt_pct, momentum_pct]


def bullet_chart_from_xls(corp_name):

    results = get_scores(corp_name)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta", value = results['ind3']['score'],
        delta = {'reference': results['ind3']['sector_score']},
        domain = {'x': [0.25, 1], 'y': [0.05, 0.25]},
        title = {
            'text': "<b>Momentum</b>",
            'font': {'size': 15}
        },
        gauge = {
            'shape': "bullet",
            'axis': {'range': [None, 5]},
            'threshold': {
                'line': {'color': "red", 'width': 5},
                'thickness': 0.75,
                'value': results['ind3']['sector_score']},
            'steps': [
                {'range': [0, 2.5], 'color': "#ed453b"},
                {'range': [2.5, 4.0], 'color': "#ecb27e"},
                {'range': [4.0, 5.0], 'color':'#e0e0a3'}],
            'bar': {'color': "#003200",
                    'thickness': 0.40}}))

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta", value = results['ind2']['score'],
        delta = {'reference': results['ind2']['sector_score']},
        domain = {'x': [0.25, 1], 'y': [0.4, 0.6]},
            title = {
            'text': "<b>Seriousness</b>",
            'font': {'size': 15}
        },
        gauge = {
            'shape': "bullet",
            'axis': {'range': [None, 5]},
            'threshold': {
                'line': {'color': "red", 'width': 5},
                'thickness': 0.75,
                'value': results['ind2']['sector_score']},
            'steps': [
                {'range': [0, 2.5], 'color': "#ed453b"},
                {'range': [2.5, 4.0], 'color': "#ecb27e"},
                {'range': [4.0, 5.0], 'color':'#e0e0a3'}],
            'bar': {'color': "#003200",
                    'thickness': 0.40}}))

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta", value = results['ind1']['score'],
        delta = {'reference': results['ind1']['sector_score']},
        domain = {'x': [0.25, 1], 'y': [0.7, 0.9]},
        title = {
            'text': "<b>Transparency</b>",
            'font': {'size': 15}
        },
        gauge = {
            'shape': "bullet",
            'axis': {'range': [None, 5]},
            'threshold': {
                'line': {'color': "red", 'width': 5},
                'thickness': 0.75,
                'value': results['ind1']['sector_score']},
            'steps': [
                {'range': [0, 2.5], 'color': "#ed453b"},
                {'range': [2.5, 4.0], 'color': "#ecb27e"},
                {'range': [4.0, 5.0], 'color':'#e0e0a3'}],
            'bar': {'color': "#003200",
                    'thickness': 0.40}}))
    fig.update_layout(height = 300, margin = {'t':0, 'b':0, 'l':0})
    
    plot_div = plot(fig, 
                    output_type='div')
    return plot_div


def get_scores(company_name):
    
    results = {
        "ind1":{
        "name":"Transparency",
        "score": 4.5,
        "sector_score": 4.2,
        },
        "ind2":{
            "name":"Seriousness",
            "score": 3.5,
            "sector_score": 3.2,
        },
        "ind3":{
            "name":"Momentum",
            "score": 2.5,
            "sector_score": 2.8,
        },
    }
    return results