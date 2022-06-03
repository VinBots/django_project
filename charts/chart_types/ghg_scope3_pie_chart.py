import pandas as pd
import plotly.graph_objs as go
import os
import sys
from pathlib import Path


def ghg_scope3_pie_chart_from_xls(company_id, params):
    """
    Builds a pie bar chart with Scope 3 GHG emissions
    Return a plotly figure
    """

    path = Path(os.path.dirname(os.getcwd()))
    XLSX_PATH = os.path.join(path.parent, "sp100.xlsx")

    sheetname = "ghg_quant"
    all_data = pd.read_excel(
        XLSX_PATH,
        sheet_name=sheetname,
        engine="openpyxl",
    )

    cond1 = all_data["company_id"] == company_id
    cond2 = all_data["Source"].isin(["Final"])
    cond3 = all_data["ghg_scope3_total"] > 0
    filter_conditions = cond1 & cond2 & cond3
    record_data = (
        all_data.loc[filter_conditions]
        .reset_index()
        .sort_values("reporting_year", ascending=False)
    )

    if len(record_data) == 0:
        return None

    reporting_year = record_data[["reporting_year"]].iloc[0, 0]

    scope3_fields = [
        "ghg_purch_scope3",
        "ghg_capital_scope3",
        "ghg_fuel_energy_loc_scope3",
        "ghg_fuel_energy_mkt_scope3",
        "ghg_upstream_td_scope3",
        "ghg_wate_ops_scope3",
        "ghg_bus_travel_scope3",
        "ghg_commute_scope3",
        "ghg_up_leased_scope3",
        "ghg_downstream_td_scope3",
        "ghg_proc_sold_scope3",
        "ghg_use_sold_scope3",
        "ghg_eol_sold_scope3",
        "ghg_down_leased_scope3",
        "ghg_franchises_scope3",
        "ghg_investments_scope3",
    ]

    scope3_fields_readable = [
        "1: Purchased Goods and Services",
        "2: Capital Goods",
        "3: Fuel- and Energy-Related Activities",
        "4: Upstream Transportation and Distribution",
        "5: Waste Generated in Operations",
        "6: Business Travel",
        "7: Employee Commuting",
        "8: Upstream Leased Assets",
        "9: Downstream Transportation and Distribution",
        "10: Processing of Sold Products",
        "11: Use of Sold Products",
        "12: End-of-Life Treatment of Sold Products",
        "13: Downstream Leased Assets",
        "14: Franchises",
        "15: Investments",
    ]
    scope3_upstream_colors = [
        "#ffbaba",
        "#ff7b7b",
        "#ff5252",
        "#ff0000",
        "#a70000",
        "#ff0000",
        "#ff4d00",
        "#ff7400",
    ]
    scope3_downstream_colors = [
        "#0000ff",
        "#3232ff",
        "#6666ff",
        "#7f7fff",
        "#9999ff",
        "#ccccff",
        "#e5e5ff",
    ]
    scope3_colors = scope3_upstream_colors + scope3_downstream_colors

    pie_data = record_data[scope3_fields].iloc[0, :]
    print(pie_data)

    labels = scope3_fields_readable
    values = pie_data
    data = [go.Pie(labels=labels, values=values, sort=False)]

    layout = go.Layout(
        title_text="",
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, b=50, t=50, pad=4),
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(
                text="<b>Scope 3</b><br>Emissions<br>Y" + str(int(reporting_year)),
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False,
            )
        ],
    )
    config = {"displaylogo": False}

    fig = go.Figure(data=data, layout=layout)

    fig.update_traces(hole=0.4)
    fig.update_traces(
        marker=dict(colors=scope3_colors, line=dict(color="#000000", width=2))
    )

    return fig
