from corporates.models.corp import Corporate
from corporates.models.ghg import GHGQuant
from corporates.models.external_sources.tradingview import Tradingview
from corporates.models.choices import Options
from corporates.management.utilities import is_ghg_fully_reported


def calculate_ghg_metrics(company, year):

    if isinstance(company, int):
        company_obj = Corporate.objects.get(company_id=company)
        company_id = company
    else:
        company_obj = company
        company_id = company.company_id

    if is_ghg_fully_reported(company, [year]):

        intensity = s3_intensity = s3_to_s1s2_ratio = None

        revenue = Tradingview.objects.get_value(
            company=company, account="Total revenue", period=year
        )
        s3_ghg = GHGQuant.objects.get_ghg(
            id=company_id, scope_coverage=Options.SCOPE3_BEST, year=year
        )

        if revenue and s3_ghg and revenue > 0:
            s3_intensity = 1e6 * s3_ghg / revenue

        s1s2_ghg = GHGQuant.objects.get_ghg(
            id=company_id, scope_coverage=Options.SCOPE12_BEST, year=year
        )
        if s3_ghg and s1s2_ghg and s1s2_ghg > 0:
            s3_to_s1s2_ratio = s3_ghg / s1s2_ghg

            if revenue and revenue > 0:
                intensity = 1e6 * (s3_ghg + s1s2_ghg) / revenue

        return dict(
            company=company_obj,
            year=year,
            intensity=intensity,
            s3_intensity=s3_intensity,
            s3_to_s1s2_ratio=s3_to_s1s2_ratio,
        )
