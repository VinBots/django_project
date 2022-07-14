from corporates.models.corp import Corporate
from corporates.models.verification import Verification
from corporates.models.ghg import GHGQuant
from corporates.models.metrics import GHGMetrics
from corporates.models.choices import Options


def parse_extract(options):

    company_id = options.get("company_id", None)
    if company_id:
        company_id_list = [company_id]
    else:
        company_id_list = Corporate.objects.values_list("company_id", flat=True)

    return {"company_id_list": company_id_list}


def is_ghg_fully_reported(company, years):

    query = Verification.objects.filter(
        company=company,
        reporting_year__in=years,
        scope12_reporting_completeness=Options.FULL,
        scope3_reporting_completeness=Options.FULL,
    )

    return query.exists()


def get_s1s2_best(company, year):
    return GHGQuant.objects.get_ghg(
        id=company.company_id, scope_coverage=Options.SCOPE12_BEST, year=year
    )


def get_s3_best(company, year):
    return GHGQuant.objects.get_ghg(
        id=company.company_id, scope_coverage=Options.SCOPE3_BEST, year=year
    )


def is_s1s2_fully_reported(company, year):
    query = Verification.objects.filter(
        company=company,
        reporting_year=year,
        scope12_reporting_completeness=Options.FULL,
    ).order_by("-last_update")
    # print(query)

    return query.exists()


def is_attribute(company, year, attribute="s3_to_s1s2_ratio"):
    # print(f"YEAR = {year}")
    result = GHGMetrics.objects.get_last_metrics(company, year)
    # print(f"result is {result}")
    # print(f"attribute is {getattr(result, attribute)}")
    return result and getattr(result, attribute)


def get_metrics_attribute(company, year, attribute="s3_to_s1s2_ratio"):
    result = GHGMetrics.objects.get_last_metrics(company, year)
    return getattr(result, attribute)
