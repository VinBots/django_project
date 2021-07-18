import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
from plotly.offline import plot

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

def bullet_chart_from_xls(corp_name):

    results = get_scores(corp_name)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta", value = results['ind3']['score'],
        delta = {'reference': results['ind3']['sector_score']},
        domain = {'x': [0.25, 1], 'y': [0.10, 0.30]},
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
        domain = {'x': [0.25, 1], 'y': [0.35, 0.55]},
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
        domain = {'x': [0.25, 1], 'y': [0.6, 0.8]},
        title = {
            'text': "<b>Transparency</b>",
            'font': {'size': 15},
            }
        ,
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

    fig.update_layout(margin = {'t':0, 'b':0, 'l':0})
    
    name_fig = "bullet_scores_{}".format(corp_name)
    fig.write_image("../django_project/static/django_project/images/charts/{}.svg".format(name_fig), scale=3, height = 300)
    plot(fig, filename = '../django_project/static/django_project/images/html_exports/{}.html'.format(name_fig), auto_open=False)

if __name__ == "__main__":
    bullet_chart_from_xls("3m")