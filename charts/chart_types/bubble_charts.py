import pandas as pd
import plotly.graph_objs as go
import os
from pathlib import Path


def bubble_chart_from_xls(company_id, params):
    
    path = Path(os.path.dirname (os.getcwd()))
    XLSX_PATH = os.path.join(path.parent, 'sp100.xlsx')
    
    COLS_TO_USE = {
    'companies':['company_id', 'company_name'],
    'ghg_quant':['company_id', 'ghg_scope_1','ghg_loc_scope_2','ghg_mkt_scope_2', 'reporting_year', "Source"],
    'grouping':['company_id', 'Sector1'],
    'financials':['company_id', 'Revenue_num_tradingview']
    }

    all_df = []
    for sheetname, cols in COLS_TO_USE.items():
        all_df.append(pd.read_excel(
            XLSX_PATH, 
            sheet_name = sheetname,
            engine = 'openpyxl', 
            usecols = cols
            ))
    merged_df = all_df[0]
    for i in range(len(COLS_TO_USE) - 1):
        merged_df = pd.merge(
            left = merged_df,
            right = all_df[i+1],
            how="left",
            on="company_id"
        )
    # Select Final Figures and Year 2019
    cond1 = (merged_df['reporting_year'] == 2019)
    cond2 = (merged_df['Source']== 'Final')
    filter_cond = cond1 & cond2
    merged_df = merged_df.loc[filter_cond]

    a =  merged_df[merged_df['company_id']==company_id]['Sector1']
    if len(a) > 0:
        sector = a.iloc[0]
    merged_df_sector = merged_df.loc[merged_df['Sector1']==sector]

    scope1 = pd.to_numeric(merged_df_sector['ghg_scope_1'], errors = 'coerce')
    scope2_loc = pd.to_numeric(merged_df_sector['ghg_loc_scope_2'], errors = 'coerce')
    scope2_mkt = pd.to_numeric(merged_df_sector['ghg_mkt_scope_2'], errors = 'coerce')

    merged_df_sector = merged_df_sector.assign(scope1_plus_scope2_loc= scope1 + scope2_loc)
    merged_df_sector = merged_df_sector.assign(scope1_plus_scope2_mkt= scope1 + scope2_mkt)
    merged_df_sector['scope1_plus_scope2'] = merged_df_sector[['scope1_plus_scope2_loc','scope1_plus_scope2_mkt']].min(axis=1)

    fields = ['company_id','company_name','ghg_scope_1', 'Sector1','Revenue_num_tradingview','scope1_plus_scope2']
    merged_df_sector = merged_df_sector [fields]

    merged_df_sector = merged_df_sector.dropna()
    merged_df_sector = merged_df_sector.assign(intensity=merged_df_sector['scope1_plus_scope2'] / merged_df_sector['Revenue_num_tradingview'])
    if len(merged_df_sector[merged_df_sector['company_id']==company_id]['company_name']) == 0:
        return None

    corp_x = merged_df_sector[merged_df_sector['company_id']==company_id]['scope1_plus_scope2'].iloc[0]
    corp_y = merged_df_sector[merged_df_sector['company_id']==company_id]['Revenue_num_tradingview'].iloc[0]
    corp_name = merged_df_sector[merged_df_sector['company_id']==company_id]['company_name'].iloc[0]
    x0 = merged_df_sector['scope1_plus_scope2']
    y0 = merged_df_sector['Revenue_num_tradingview']
    intensity_data = 10000000 * merged_df_sector['intensity']
    #index_corp = merged_df_sector.loc[merged_df_sector['company_id'] == company_id].index
    #merged_df_sector.drop(index_corp , inplace=True)
    x_median_x = [x0.min(), x0.max()]
    y_median_x = [y0.median(), y0.median()]
    x_median_y = [x0.median(), x0.median()]
    y_median_y = [y0.min(), y0.max()]

    layout = go.Layout (
        title = '<b>Operational Emissions Intensity Benchmark</b><br>Sector: ' + sector,
        title_x = 0.5,
        titlefont = dict(
            family = 'Arial',
            size = 16),
        plot_bgcolor = 'antiquewhite',
        xaxis =  dict(
            autorange = "reversed",
            type = 'log',
            title = '<i>high</i>----------<b>Scope1+2 Emissions</b>----------<i>low</i>'),
        yaxis = dict(
            type = 'log',
            title = 'Revenue'),
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

    trace3 = go.Scatter(
        x=merged_df_sector['scope1_plus_scope2'], 
        y=merged_df_sector['Revenue_num_tradingview'],
        showlegend = False,
        name="benchmark", 
        text=merged_df_sector['company_name'],
        mode = 'markers+text',
        line = {'color':'black'}, 
        marker = dict (
            color=intensity_data,
            size=25,
            showscale=True,
            colorscale='Hot_r',
            line=dict(
                    color='black',
                    width=1,
                )

            ),
        hovertemplate = '%{text}<br><b>Revenue:</b>%{y}'+ '<br><b>Emissions:</b> %{x:.2s}', # + '<br><b>Intensity: </b> %{intensity_data}',
        textposition='top center'
        )

    fig = go.Figure(data = [trace1, trace2, trace3], 
                    layout = layout)
                    
    
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[corp_x],
            y=[corp_y],
            text = [corp_name],
            marker=dict(
                color='rgba(255,0,0, 0.01)',#'rgba(135, 206, 250, 0.01)',
                size=25,
                line=dict(
                    color='red',
                    width=3,
                )
            ),
            
            hovertemplate = '%{text}<br><b>Revenue:</b>%{y}'+ '<br><b>Emissions:</b> %{x:.2s}', # + '<br><b>Intensity: </b> %{intensity_data}',
            showlegend=False
        )
    )
    
    #full_fig = fig.full_figure_for_development(warn=False)
                    
    fig.update_layout(
        autosize=False,
        width=2000,
        height=1000,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=80,
            pad=4
        ),
        paper_bgcolor="#eeebf0",
        plot_bgcolor = '#eeebf0',
    )

    return fig