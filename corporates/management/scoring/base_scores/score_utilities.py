import json

from corporates.models import GHGQuant
from corporates.utilities import get_last_x_years, get_forward_looking_reduction


def get_forward_looking_target(company_id, selected_target, baseline):

    last_reporting_year = GHGQuant.objects.get_last_reporting_year(
        company_id=company_id
    )
    if not last_reporting_year or not last_reporting_year in get_last_x_years(x=2):
        error_msg = (
            f"No GHG Inventory found over the past 2 years {get_last_x_years(x=2)}"
        )
        return None, {"error_msg": error_msg}

    last_reporting_year_ghg = GHGQuant.objects.get_ghg(
        company_id,
        selected_target.scope_coverage,
        last_reporting_year,
    )
    if not last_reporting_year_ghg or last_reporting_year_ghg <= 0:
        error_msg = (
            f"last reporting year {last_reporting_year} GHG is not a positive number"
        )
        return None, {"error_msg": error_msg}

    test_result, all_tests = selected_target.fl_red_data_check(last_reporting_year)

    if not test_result:
        error_msg = json.dumps(all_tests)
        return None, {"error_msg": error_msg}

    fl_red = get_forward_looking_reduction(
        last_reporting_year=last_reporting_year,
        last_reporting_year_ghg=last_reporting_year_ghg,
        baseline=baseline,
        reduction_obj=selected_target.reduction_obj,
        target_year=selected_target.target_year,
    )
    meta_msg = {
        "last_reporting_year": last_reporting_year,
        "last_reporting_year_ghg": last_reporting_year_ghg,
    }
    return fl_red, meta_msg
