import pandas as pd
import plotly.graph_objs as go
import os


def bubble_chart_from_xls(company_id, params):
    ghg_sheetname = "GHG" + params["year"][-2:]
    XLSX_PATH = os.path.join ('../django_project/static/django_project', 'data', 'sp100_data.xlsx')
    COLS_TO_USE = {
        'companies':['company_id', 'company_name'],
        'GHG19':['company_id', 'gross_total_scope1', 'gross_scope2_calc'],
        'grouping':['company_id', 'Sector1'],
        'financials':['company_id', 'Revenue']
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
    get_sector = merged_df[merged_df['company_id']==company_id]['Sector1']
    if len(get_sector) > 0:
        sector = get_sector.iloc[0]
    else:
        return False
    
    merged_df_sector = merged_df.loc[merged_df['Sector1']==sector]
    
    scope1 = pd.to_numeric(merged_df_sector['gross_total_scope1'], errors = 'coerce')
    scope2 = pd.to_numeric(merged_df_sector['gross_scope2_calc'], errors = 'coerce')
    merged_df_sector = merged_df_sector.assign(scope1_plus_scope2= scope1 + scope2)
    merged_df_sector = merged_df_sector.dropna()
    
    get_corp_name = merged_df_sector[merged_df_sector['company_id']==company_id]['company_name']
    if len(get_corp_name) > 0:
        corp_x = merged_df_sector[merged_df_sector['company_id']==company_id]['scope1_plus_scope2'].iloc[0]
        corp_y = merged_df_sector[merged_df_sector['company_id']==company_id]['Revenue'].iloc[0]
        corp_name = merged_df_sector[merged_df_sector['company_id']==company_id]['company_name'].iloc[0]
        trace4 = go.Scatter(
            x=[corp_x], 
            y=[corp_y],
            showlegend = False,
            name=corp_name, 
            text= corp_name,
            textfont=dict(
                size=6,
                color="#de425b"),
            mode = 'markers+text',
            line = {'color':'#de425b'}, 
            marker = {
                'color': '#de425b',
                'opacity': 1,
                'size':20
            },
            textposition='top center'
            )
    else:
        trace4 = go.Scatter()
    
    
    x0 = merged_df_sector['scope1_plus_scope2']
    y0 = merged_df_sector['Revenue']
    index_corp = merged_df_sector.loc[merged_df_sector['company_id'] == company_id].index
    merged_df_sector.drop(index_corp , inplace=True)



    layout = go.Layout (
        title = '<b>GHG Emissions vs. Revenue</b><br>Sector: ' + sector,
        title_x = 0.5,
        font = dict(
            size = 6,
        ),
        titlefont = dict(
            family = 'Arial',
            size = 12),
        #plot_bgcolor = 'antiquewhite',
        xaxis =  dict(
            autorange = "reversed",
            type = 'log',
            title = '<i>high</i>----------<b>Scope1+2 Emissions</b>----------<i>low</i>',
            ),
        yaxis = dict(
            type = 'log',
            title = 'Revenue',
            ))

    trace3 = go.Scatter(
        x=merged_df_sector['scope1_plus_scope2'], 
        y=merged_df_sector['Revenue'],
        showlegend = False,
        name="benchmark", 
        text=merged_df_sector['company_name'],
        textfont=dict(
                size=6,),
        mode = 'markers+text',
        line = {'color':'black'}, 
        marker = {
            'color': '#488f31',
            'opacity': 0.4,
            'size':12
        },
        textposition='top center'
        )
    

    fig = go.Figure(data = [trace3, trace4], 
                    layout = layout)
    full_fig = fig.full_figure_for_development()
    x_range = full_fig.layout.xaxis.range
    y_range = full_fig.layout.yaxis.range
    
    x_median_x = [10**x_range[0], 10**x_range[1]]
    y_median_x = [y0.median(), y0.median()]
    x_median_y = [x0.median(), x0.median()]
    y_median_y = [10**y_range[0], 10**y_range[1]]



    fig.add_trace (go.Scatter(x=x_median_y, 
                            y=y_median_y, 
                            showlegend = False, 
                            name='Median y',
                            mode = "lines",
                            line = {
                                'color':'gray',
                                'width':5, 
                                'dash':'dash'
                                }
                                ))

    fig.add_trace(go.Scatter(x=x_median_x, 
                            y=y_median_x, 
                            showlegend = False, 
                            name='Median x', 
                            mode = "lines",
                            line = {
                                'color':'gray', 
                                'width':5, 
                                'dash':'dash'
                                }
                            ))


    



    fig.add_shape(type="rect",
            x0=x0.median(), y0=y0.median(), x1=10**x_range[1], y1=10**y_range[1],
            line=dict(color="orange",width=0.5, dash="dot"), fillcolor="green", opacity=0.2,
            layer="below"
        )

    fig.add_shape(type="rect",
        x0=10**x_range[0], y0=10**y_range[0], x1=x0.median(), y1=y0.median(),
        line=dict(color="orange",width=0.5, dash="dot"), fillcolor="red", opacity=0.2,
        layer="below"
    )
    fig.add_shape(type="rect",
        x0=10**x_range[0], y0=y0.median(), x1=x0.median(), y1=10**y_range[1],
        line=dict(color="orange",width=0.5, dash="dot"), fillcolor="orange", opacity=0.2,
        layer="below"
    )
    fig.add_shape(type="rect",
        x0=x0.median(), y0=10**y_range[0], x1=10**x_range[1], y1=y0.median(),
        line=dict(color="orange",width=0.5, dash="dot"), fillcolor="orange", opacity=0.2,
        layer="below"
    )
    
                    
    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=80,
            pad=4
        ),
        #paper_bgcolor="#bad0af",
        plot_bgcolor = 'white',#'#f1f1f1',
    )
    
    return fig