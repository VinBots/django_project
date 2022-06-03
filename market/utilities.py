import datetime

from corporates.models import (
    LatestCompanyScore,
    Corporate,
    StockData,
    Tradingview,
    MSCI,
    CO2Pricing,
    CorporateGrouping,
    CalcMetrics,
)


def get_financials(company_id, account, period):
    query = Tradingview.objects.get_last_tv_value(
        company=company_id, account=account, period=period
    )
    if query:
        return query.value
    else:
        return None


def get_MSCI_ITR(company_id):
    query = MSCI.objects.get_last_msci_value(company=company_id)
    if query:
        return query.ITR
    else:
        return None


def get_stock(company_id, current_date, attribute):
    query = StockData.objects.get_last_stock_data(
        company=company_id, current_date=current_date
    )
    if query:
        return getattr(query, attribute)
    else:
        return None


def get_dates_available():
    query = StockData.objects.all().order_by("-current_date")
    if query.exists():
        return query.values_list("current_date", "last_date")[0]


def get_co2_price(date):
    query = CO2Pricing.objects.get_last_co2_price(date=date)
    if query:
        return query.price


def get_year_end_co2_price(year="2021"):

    DEFAULT_PRICE = 51.4501
    date_str = "12-31-" + year
    format_str = "%m-%d-%Y"
    date_obj = datetime.datetime.strptime(date_str, format_str).date()
    price = get_co2_price(date_obj)

    if price:
        return price
    else:
        return DEFAULT_PRICE


def get_market_stats():
    """
    Fetch companies market statistics information
    """

    data = []
    sp100_company_ids = CorporateGrouping.objects.get_sp100_company_ids()

    year_end_co2_price = get_year_end_co2_price(year="2021")
    current_date_available, last_date_available = get_dates_available()
    co2_price_current = get_co2_price(current_date_available)
    co2_price_last = get_co2_price(date=last_date_available)

    for company_id in sp100_company_ids:

        total_footprint_query = CalcMetrics.objects.get_last_metrics(
            company=company_id, year="2020", metrics="total_ghg_estimate"
        )
        if total_footprint_query:
            total_footprint = total_footprint_query.value
        else:
            total_footprint = 0
        last_price_year_end = get_stock(company_id, "2021-12-31", "current_c")
        current_c = get_stock(company_id, current_date_available, "current_c")
        ebitda = get_financials(company_id=company_id, account="EBITDA", period=2021)
        pre_pct_chg = get_stock(company_id, current_date_available, "pre_pct_chg")
        ebitda_exp_t1 = get_ebitda_exposures(total_footprint, ebitda, co2_price_current)
        ebitda_exp_t0 = get_ebitda_exposures(total_footprint, ebitda, co2_price_last)
        ebitda_exp_t_year_end = get_ebitda_exposures(
            total_footprint, ebitda, co2_price=year_end_co2_price
        )
        revenue = get_financials(
            company_id=company_id, account="Total revenue", period=2021
        )
        pre_ytd_chg = calculate_pre_ytd_chg(current_c, last_price_year_end)

        company_dict = {
            "company_id": company_id,
            "company_name": get_company_name(company_id),
            "score_db": get_score_value(company_id),
            "current_c": current_c,
            "pre_pct_chg": round(pre_pct_chg, 2),
            "current_date": current_date_available,
            "Revenue": revenue,
            "EBITDA": ebitda,
            "ITR": get_MSCI_ITR(company_id=company_id),
            "total_footprint": int(total_footprint),
            "pre_ytd_chg": pre_ytd_chg,
            "rev_co2_exposure": calculate_revenue_exposure(
                total_footprint, revenue, co2_price_current
            ),
            "ebitda_exp_t1": ebitda_exp_t1,
            "ebitda_exp_t0": ebitda_exp_t0,
            "ebitda_exp_t_year_end": ebitda_exp_t_year_end,
            "post_pct_chg": calculate_post_daily_change(
                pre_pct_chg, ebitda_exp_t1, ebitda_exp_t0
            ),
            "post_ytd_chg": calculate_post_ytd_change(
                pre_ytd_chg, ebitda_exp_t1, ebitda_exp_t_year_end
            ),
        }
        data.append(company_dict)

    return data


def get_meta_data():

    current_date_available, last_date_available = get_dates_available()

    return {
        "current_date": current_date_available,
        "last_date": last_date_available,
        "co2_price_current": CO2Pricing.objects.get_last_co2_price(
            date=current_date_available
        ),
        "co2_price_last": CO2Pricing.objects.get_last_co2_price(
            date=last_date_available
        ),
    }


def get_company_name(company_id):
    return Corporate.objects.filter(company_id=company_id).values_list(
        "name", flat=True
    )[0]


def get_score_value(company_id):

    query = LatestCompanyScore.objects.get_latest_company_score_value(
        company_id=company_id, score_name="Score_total"
    )
    if query:
        return query.values_list("score_value", flat=True)[0]


def calculate_pre_ytd_chg(current_c, last_price_year_end):
    if current_c and last_price_year_end:
        pre_ytd_chg = (current_c / last_price_year_end - 1) * 100
        return round(pre_ytd_chg, 2)


def get_ebitda_exposures(carbon_footprint, ebitda, co2_price=50):
    if ebitda and co2_price and carbon_footprint:
        return round(100 * co2_price * carbon_footprint / (ebitda), 2)


def calculate_revenue_exposure(carbon_footprint, revenue, co2_price=50):
    if revenue and co2_price and carbon_footprint:
        return round(100 * co2_price * carbon_footprint / (revenue), 2)


def calculate_post_daily_change(pre_pct_chg, ebitda_exp_t1, ebitda_exp_t0):
    if pre_pct_chg and ebitda_exp_t1 and ebitda_exp_t0:
        return round(
            (
                (pre_pct_chg / 100 + 1)
                * (1 - ebitda_exp_t1 / 100)
                / (1 - ebitda_exp_t0 / 100)
                - 1
            )
            * 100,
            2,
        )


def calculate_post_ytd_change(pre_ytd_chg, ebitda_exp_t1, ebitda_exp_t_year_end):
    if pre_ytd_chg and ebitda_exp_t1 and ebitda_exp_t_year_end:
        return round(
            (
                (pre_ytd_chg / 100 + 1)
                * (1 - ebitda_exp_t1 / 100)
                / (1 - ebitda_exp_t_year_end / 100)
                - 1
            )
            * 100,
            2,
        )
