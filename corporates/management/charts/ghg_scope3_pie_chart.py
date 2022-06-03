import pandas as pd
import plotly.graph_objs as go

from corporates.models.ghg import GHGQuant
from corporates.models.choices import Options


def ghg_scope3_pie_chart_from_db(company_id, params):
    """
    Builds a pie bar chart with Scope 3 GHG emissions
    Return a plotly figure
    """

    queryset = GHGQuant.objects.filter(
        company__company_id=company_id, source=Options.FINAL
    ).order_by("-reporting_year")
    print(queryset)

    if not queryset.exists():
        return None

    queryset = [x for x in queryset if x.scope_3_loc_agg > 0]
    if not queryset:
        return None

    result = queryset[0]
    print(f"The result of the query is {result} of type {type(result)}")

    reporting_year = result.reporting_year
    print(f"The reporting_year is {reporting_year}")

    scope3_fields = [
        "ghg_purch_scope3",
        "ghg_capital_scope3",
        "ghg_fuel_energy_loc_scope3",
        "ghg_fuel_energy_mkt_scope3",
        "ghg_upstream_td_scope3",
        "ghg_waste_ops_scope3",
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

    pie_data = [getattr(result, field) for field in scope3_fields]
    pie_data = list(map(lambda x: x if x > 0 else "", pie_data))

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
