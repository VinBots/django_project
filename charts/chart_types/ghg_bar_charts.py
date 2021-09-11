import pandas as pd
import plotly.graph_objs as go
import os
from pathlib import Path

def ghg_bar_chart_from_xls(company_id, params):
    """
    Builds a bar chart with GHG emissions by scope by year
    Return a plotly figure
    """

    path = Path(os.path.dirname (os.getcwd()))
    XLSX_PATH = os.path.join(path.parent, 'sp100.xlsx')

    sheetname = 'ghg_s1s2_chart'
    df = pd.read_excel(
    XLSX_PATH, 
    sheet_name = sheetname,
    engine = 'openpyxl',
    )

    is_target = False
    df = df.loc[(df['company_id']==company_id) & (df['year_n'].notna())]

    if len(df.loc[(df['ctrl_target_year']==True) & (df['target_year'] > df['year_n'])]) > 0:
        is_target = True

    if len(df) > 0:
        scope1_list = df[['ghg_scope1_n-2','ghg_scope1_n-1','ghg_scope1_n']].values[0].tolist()
        scope2_list = df[['ghg_scope2_n-2','ghg_scope2_n-1','ghg_scope2_n']].values[0].tolist()
        #base_target_list = df[['baseline','ghg_target']].values[0].tolist()
        year_n = df[['year_n']].iloc[0,0]
        scope2_type = df[['scope2_type']].iloc[0,0]

        if is_target:

            target_year = df[['target_year']].iloc[0,0]
            baseline_year = df[['baseline_year']].iloc[0,0]
            target_data = df[['ghg_target']].values[0].tolist()

            filler_left = False
            baseline_data = []
            trace_filler_left = []

            if baseline_year < year_n -2:
                baseline_data = df[['baseline']].values[0].tolist()
                filler_left = True

            filler_right_data = []
            if target_year - year_n == 4:
                filler_right_data = [str(int(year_n + 1)), str(int(year_n + 2)), str(int(target_year - 1))]
            elif target_year - year_n > 4:    
                filler_right_data = [str(int(year_n + 1)), "...", str(int(target_year - 1))]
            elif target_year - year_n == 3:
                filler_right_data = [str(int(year_n + 1)), str(int(year_n + 2))]
            elif target_year - year_n == 2:
                filler_right_data = [str(int(year_n + 1))]
                    
            red_obj = round(df[['ghg_target_reduction_obj']].iloc[0,0]*100,1)

            trace_baseline = go.Bar(
                x = ["<b>Baseline</b><br>(Y"+str(int(baseline_year))+")"],
                y = baseline_data,
                name = 'Baseline',
                marker_color='dimgrey',
                showlegend=False,
                text = baseline_data,
                textposition='outside',
                texttemplate="<b>%{text:.2s}</b>",
                hovertemplate = '<b>Scope:</b> 1-2<br>'+ '<b>Year:</b> %{x}<br>' + '<b>Emissions:</b> %{y}',
                )

            if filler_left:
                trace_filler_left = go.Bar(
                    x = ["."],
                    y = [0],
                    showlegend=False,
                    )

            trace_filler_right =  go.Bar (
                x = filler_right_data,
                y = [0] * len(filler_right_data),
                showlegend=False,
                )

        trace_scope12_x = ["Y" + str(int(year_n-2)), "Y" + str(int(year_n-1)), "Y" + str(int(year_n))]

        trace_scope1 = go.Bar(
            x = trace_scope12_x,
            y = scope1_list,
            name = 'scope 1',
            marker_color = '#2000b1',
            textposition='auto',
            text = ["" if i==0 else i for i in scope1_list],
            texttemplate=["" if i==0 else "%{text:.2s}" for i in scope1_list],
            hovertemplate = '<b>Scope:</b> 1 (direct)<br>'+ '<b>Year:</b> %{x}<br>' + '<b>Emissions:</b> %{y}',
            )

        trace_scope2 = go.Bar(
            x = trace_scope12_x,
            y = scope2_list,
            name = "scope 2<br>("+scope2_type+"-based)",
            marker_color='#2000b1',
            opacity = 0.7,
            text = ["" if i==0 else i for i in scope2_list],
            textposition='auto',
            texttemplate=["" if i==0 else "%{text:.2s}" for i in scope2_list],
            hovertemplate = '<b>Scope:</b> 2 (indirect)<br>'+ '<b>Year:</b> %{x}<br>' + '<b>Emissions:</b> %{y}',
            )

        if is_target:
            trace_target = go.Bar(
                x = ["<b>Target</b><br>(Y"+str(int(target_year))+")"],
                y = target_data,
                name = 'Target',
                marker_color=['#b1002c'],
                showlegend=False,
                text = target_data,
                textposition='inside',
                texttemplate="<b>%{text:.2s}</b>",
                hovertemplate = '<b>Scope:</b> 1-2<br>'+ '<b>Year:</b> %{x}<br>' + '<b>Emissions:</b> %{y}',
                )

        if is_target:
            
            if filler_left:
                data = [trace_baseline, trace_filler_left, trace_scope1, trace_scope2, trace_filler_right, trace_target]
            else:
                data = [trace_baseline, trace_scope1, trace_scope2, trace_filler_right, trace_target]
        else:
            data = [trace_scope1, trace_scope2]
        layout = go.Layout (
            barmode = 'stack',
            title = '<b>Operational Emissions (S1+S2) Evolution</b><br>',
            title_x = 0.5,
            titlefont = dict(
                family = 'Arial',
                size = 16),
                xaxis =  dict(
                    type = 'category',
                    title = ''),
                yaxis = dict(
                    title = 'Emissions (in tons of CO<sub>2</sub>e)'),    
            legend=dict(
                title="<b>Emissions</b>",
                orientation="v",
                traceorder="normal"),
            autosize=False,
            margin=dict(
                l=50,
                r=50,
                b=50,
                t=80,
                pad=4
            )
        )
        config = {'displaylogo': False}

        fig = go.Figure(
            data=data,
            layout = layout
            )

        if is_target:
            fig.add_shape(
                type='line',
                line = dict(color='#b1002c', dash='dot'),
                xref='x',
                yref='y',
                x0=0.4,
                y0= target_data[0],
                x1=7.6,
                y1=target_data[0],
            )

            fig.add_annotation(
                x="<b>Target</b><br>(Y"+str(int(target_year))+")",
                y= target_data[0],
                xanchor="right",
                text = "Reduction Objectives<br><b>-"+str(red_obj)+"%</b> vs. "+str(int(baseline_year)),
                bgcolor = "wheat",
                bordercolor= "red",
                borderwidth=1,
            )
        year_index = 0
        for i,j in zip (scope1_list, scope2_list):
            if (i ==0) or (j == 0):
                if i+j == 0:
                    warning_text = "1-2"
                elif i==0:
                    warning_text = "1"
                elif j==0:
                    warning_text = "2"
                fig.add_annotation(
                    x=trace_scope12_x[year_index],
                    y= i + j,
                    xanchor="center",
                    text = "Scope "+ warning_text + "<br>not reported",
                )
            year_index +=1
        return fig