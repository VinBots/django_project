import pandas as pd
import plotly.graph_objs as go
import os


def ghg_bar_chart_from_xls(company_id, params):
    """
    Builds a bar chart with GHG emissions by scope by year
    Return a plotly figure
    """

    years = params["years"]
    years_sheet = ['GHG'+ year[-2:] for year in years]
    
    XLSX_PATH = os.path.join ('../django_project/static/django_project', 'data', 'sp100_data.xlsx')
    COLS_TO_USE = {
        years_sheet[0]:['company_id', 'gross_total_scope1', 'gross_scope2_calc', 'gross_total_scope3'],
        years_sheet[1]:['company_id', 'gross_total_scope1', 'gross_scope2_calc', 'gross_total_scope3'],
        years_sheet[2]:['company_id', 'gross_total_scope1', 'gross_scope2_calc', 'gross_total_scope3'],
    }

    i=0
    all_df = []
    for sheetname, cols in COLS_TO_USE.items():
    
        df_by_year = pd.read_excel(
            XLSX_PATH, 
            sheet_name = sheetname,
            engine = 'openpyxl', 
            usecols = cols
            )
        df_by_year = df_by_year.loc[df_by_year['company_id'] == company_id]
        df_by_year['year'] = years[i]

        all_df.append(df_by_year)
        i+=1

    merged_df = pd.concat(
        all_df
    )

    scope1 = pd.to_numeric(merged_df['gross_total_scope1'], errors = 'coerce')
    scope2 = pd.to_numeric(merged_df['gross_scope2_calc'], errors = 'coerce')
    scope3 = pd.to_numeric(merged_df['gross_total_scope3'], errors = 'coerce')
    
    if not((scope1 > 0).any() or (scope2 > 0).any() or (scope3 > 0).any()):
        return None

    trace1 = go.Bar(
        x = years,
        y = scope1,
        name = 'Scope1',
        marker_color = '#488f31'
        )
    trace2 = go.Bar(
        x = years,
        y = scope2,
        name = 'Scope2',
        marker_color='#feba65',
        )
    trace3 = go.Bar(
        x = years,
        y = scope3,
        name = 'Scope3',
        marker_color='#de425b',
        )

    data = [trace1, trace2, trace3]

    layout = go.Layout (
        barmode='stack',
        title = '<b>GHG Emissions Evolution</b><br>',
        title_x = 0.5,
        titlefont = dict(
            family = 'Arial',
            size = 16),
            paper_bgcolor="#bad0af",
            plot_bgcolor = 'antiquewhite',
            xaxis =  dict(
            title = '<b>Reporting years</b>'),
            yaxis = dict(
                title = 'Emissions (in tons of CO2e)'),    
        legend=dict(
            title="Emissions",
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0),
        autosize=False,
        width=800,
        height=400,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=80,
            pad=4
        )
        
    )

    fig = go.Figure(
        data=data,
        layout = layout
        )

    return fig