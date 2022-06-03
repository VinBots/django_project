import logging

import pandas as pd
import plotly.graph_objs as go

from corporates.models.ghg import GHGQuant
from corporates.models.external_sources.tradingview import Tradingview
from corporates.models.grouping import CorporateGrouping, GICS
from corporates.models.choices import Options


def get_revenue(company_id, account, period):
    last_record = Tradingview.objects.get_last_tv_value(company_id, account, period)
    if last_record:
        return last_record.value


def get_sector_name(company_id):
    query = CorporateGrouping.objects.filter(company__company_id=company_id)
    if (
        not query.exists()
        or not query.values_list("gics_sub_industry_name__sector_name")[0][0]
    ):
        logging.warning(
            f"No gics_sub_industry_name was found for company with company_id = {company_id}"
        )
        return
    return query.values_list("gics_sub_industry_name__sector_name")[0][0]


def get_corporates_in_sector(sector_name):
    sub_industry_in_sector = GICS.objects.filter(sector_name=sector_name)
    return CorporateGrouping.objects.filter(
        gics_sub_industry_name__in=sub_industry_in_sector
    ).values_list("company", flat=True)


def get_ghg_data_df(corporates_in_sector):

    ghg_data = GHGQuant.objects.filter(
        company__in=corporates_in_sector, source=Options.FINAL
    ).order_by("-reporting_year")

    s1s2_best_list = [
        {
            "id": record.id,
            "s1s2": record.scope_12_best,
        }
        for record in ghg_data
    ]

    s1s2_best_df = pd.DataFrame.from_records(s1s2_best_list)

    ghg_data_df = pd.DataFrame.from_records(
        ghg_data.all().values_list(
            "id", "company__company_id", "company__name", "reporting_year"
        ),
        columns=["id", "company_id", "company_name", "reporting_year"],
    )

    return pd.merge(left=ghg_data_df, on="id", right=s1s2_best_df, how="left")


def add_revenue_df(ghg_data_df):

    revenue = [
        get_revenue(company_id, "Total revenue", period)
        for company_id, period in zip(
            ghg_data_df["company_id"],
            ghg_data_df["reporting_year"],
        )
    ]
    ghg_data_df["revenue"] = revenue
    return ghg_data_df


def add_intensity(ghg_revenue_df):

    return ghg_revenue_df.assign(
        intensity=1e6 * ghg_revenue_df["s1s2"] / ghg_revenue_df["revenue"]
    )


def is_df_valid(df, company_id):
    test1 = company_id in df["company_id"].values
    test2 = len(df.index) > 1
    return test1 & test2


def design_chart(company_id, df, sector_name):

    corp_x = df[df["company_id"] == company_id]["s1s2"].iloc[0]
    corp_y = df[df["company_id"] == company_id]["revenue"].iloc[0]
    corp_name = df[df["company_id"] == company_id]["company_name"].iloc[0]
    corp_reporting_year = df[df["company_id"] == company_id]["reporting_year"].iloc[0]
    corp_intensity = df[df["company_id"] == company_id]["intensity"].iloc[0]
    x0 = df["s1s2"]
    y0 = df["revenue"]
    intensity_data = df["intensity"]
    reporting_years = df["reporting_year"]

    x_median_x = [x0.min(), x0.max()]
    y_median_x = [y0.median(), y0.median()]
    x_median_y = [x0.median(), x0.median()]
    y_median_y = [y0.min(), y0.max()]

    layout = go.Layout(
        title="<b>Operational Emissions Intensity Benchmark</b><br>Sector: "
        + sector_name,
        title_x=0.5,
        titlefont=dict(family="Arial", size=16),
        plot_bgcolor="antiquewhite",
        xaxis=dict(
            autorange="reversed",
            type="log",
            title="<i>high</i>----------<b>Scope1+2 Emissions</b>----------<i>low</i>",
        ),
        yaxis=dict(type="log", title="Revenue"),
    )

    trace1 = go.Scatter(
        x=x_median_y,
        y=y_median_y,
        showlegend=False,
        name="Median y",
        mode="lines",
        line=dict(color="gray", width=2, dash="dash"),
    )

    trace2 = go.Scatter(
        x=x_median_x,
        y=y_median_x,
        showlegend=False,
        name="Median x",
        mode="lines",
        line={"color": "gray", "width": 2, "dash": "dash"},
    )

    trace3 = go.Scatter(
        x=df["s1s2"],
        y=df["revenue"],
        showlegend=False,
        name="",
        text=df["company_name"],
        mode="markers+text",
        line={"color": "black"},
        marker=dict(
            color=intensity_data,
            size=25,
            showscale=True,
            colorscale="Hot_r",
            line=dict(
                color="black",
                width=1,
            ),
        ),
        customdata=intensity_data,
        hovertemplate="%{text}<br><b>Revenue:</b>%{y}"
        + "<br><b>Emissions:</b> %{x:.2s}"
        # + "<br><b>Year:</b> %{customdata[0]}"
        + "<br><b>Intensity: </b> %{customdata:,.0f}",
        textposition="top center",
    )

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

    fig.add_trace(
        go.Scatter(
            mode="markers",
            x=[corp_x],
            y=[corp_y],
            name="",
            text=[corp_name],
            marker=dict(
                color="rgba(255,0,0, 0.01)",  #'rgba(135, 206, 250, 0.01)',
                size=25,
                line=dict(
                    color="red",
                    width=3,
                ),
            ),
            customdata=[corp_intensity],
            hovertemplate="%{text}<br><b>Revenue:</b>%{y}"
            + "<br><b>Emissions:</b> %{x:.2s}"
            # + "<br><b>Year:</b> %{customdata}"
            + "<br><b>Intensity: </b> %{customdata:,.0f}",
            showlegend=False,
        )
    )

    # full_fig = fig.full_figure_for_development(warn=False)

    fig.update_layout(
        autosize=True,
        # width=1000,
        # height=500,
        margin=dict(l=50, r=50, b=50, t=80, pad=4),
        paper_bgcolor="#eeebf0",
        plot_bgcolor="#eeebf0",
    )

    return fig


def bubble_chart_from_db(company_id, params):

    sector_name = get_sector_name(company_id)
    if not sector_name:
        return
    corporates_in_sector = get_corporates_in_sector(sector_name)
    ghg_data_df = get_ghg_data_df(corporates_in_sector)
    ghg_revenue_df = add_revenue_df(ghg_data_df)
    ghg_revenue_df = ghg_revenue_df.drop_duplicates(subset=["company_id"]).dropna()
    ghg_revenue_intensity_df = add_intensity(ghg_revenue_df)
    if is_df_valid(ghg_revenue_intensity_df, company_id):
        return design_chart(
            company_id=company_id, df=ghg_revenue_intensity_df, sector_name=sector_name
        )
    else:
        logging.warning(
            f"the bubble chart for company_id {company_id} could not be built because of invalid data"
        )
        logging.warning(ghg_revenue_intensity_df)
