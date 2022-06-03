from corporates.models import TargetQuant, GHGQuant
from corporates.models.choices import Options
from corporates.management.scoring.base_scores.score_utilities import (
    get_forward_looking_target,
)


def historical_perf_x(score_value, valid_target):

    meta_value = {}

    queryset = TargetQuant.objects.get_earliest_highest(
        company_id=score_value.company.company_id, valid_target=valid_target
    )
    if not queryset.exists():
        error_msg = f"No target found for {valid_target}"
        score_value.meta_value = {"error": error_msg}
        return None, meta_value

    selected_target = queryset[0]

    selected_target.get_auto_baseline()

    baseline = selected_target.get_baseline()
    if not baseline or baseline < 0:
        meta_value.update(
            {
                "error": f"No baseline for {selected_target.get_scope_coverage_display()} could be found"
            }
        )
        return None, meta_value

    base_year = selected_target.base_year
    target_year = selected_target.target_year
    reduction_obj = selected_target.reduction_obj

    last_reporting_year = GHGQuant.objects.get_last_reporting_year(
        company_id=score_value.company.company_id
    )
    if not last_reporting_year:
        meta_value.update(
            {"error": f"The last reporting year could be found in the database"}
        )
        return None, meta_value

    last_reporting_year_ghg = GHGQuant.objects.get_ghg(
        score_value.company.company_id,
        selected_target.scope_coverage,
        last_reporting_year,
    )

    if not last_reporting_year_ghg or last_reporting_year_ghg <= 0:
        meta_value.update({"error_msg": f"last_reporting_year_ghg is not valid"})
        return None, meta_value

    YTD_reduction = (-last_reporting_year_ghg / baseline + 1) * 100

    YTD_reduction_obj = (
        reduction_obj
        * (int(last_reporting_year) - int(base_year))
        / (int(target_year) - int(base_year))
    )

    if YTD_reduction_obj <= 0:
        meta_value.update(
            {
                "error_msg": f"YTD_reduction_obj is not a positive number = {float(YTD_reduction_obj *100):.2f}"
            }
        )
        return None, meta_value

    result = round(YTD_reduction / float(YTD_reduction_obj), 2)

    meta_value.update(
        {
            "ytd_reduction_actual": f"{float(YTD_reduction):.2f}",
            "ytd_reduction_objectives": f"{float(YTD_reduction_obj):.2f}",
            "total_reduction_objectives": f"{float(reduction_obj):.2f}",
        }
    )

    return result, meta_value


def momentum_perf_x(score_value, valid_target):

    meta_value = {}

    queryset = TargetQuant.objects.get_earliest_highest(
        company_id=score_value.company.company_id,
        valid_target=valid_target,
    )
    if not queryset.exists():
        error_msg = f"No target found for {valid_target}"
        score_value.meta_value = {"error": error_msg}
        return None, meta_value

    selected_target = queryset[0]

    selected_target.get_auto_baseline()

    baseline = selected_target.get_baseline()
    if not baseline:
        meta_value.update(
            {
                "error_msg": f"No baseline for {selected_target.get_scope_coverage_display()} could be found"
            }
        )
        return None, meta_value

    fl_red, meta_msg = get_forward_looking_target(
        company_id=score_value.company.company_id,
        selected_target=selected_target,
        baseline=baseline,
    )
    score_value.meta_value = meta_msg

    if not fl_red or fl_red < 0:
        meta_value.update(
            {
                "error_msg": f"Forward-looking reduction could not be calculated : {fl_red}"
            }
        )
        return None, meta_value

    last_reporting_year = GHGQuant.objects.get_last_reporting_year(
        company_id=score_value.company.company_id
    )
    last_reporting_year_ghg = GHGQuant.objects.get_ghg(
        score_value.company.company_id,
        selected_target.scope_coverage,
        last_reporting_year,
    )
    if not last_reporting_year_ghg or last_reporting_year_ghg <= 0:
        meta_value.update({"error_msg": f"last_reporting_year_ghg is not valid"})
        return None, meta_value

    preceding_year = str(int(last_reporting_year) - 1)
    preceding_year_ghg = GHGQuant.objects.get_ghg(
        score_value.company.company_id,
        selected_target.scope_coverage,
        preceding_year,
    )
    if not preceding_year_ghg or preceding_year_ghg <= 0:
        meta_value.update({"error_msg": f"preceding_year_ghg is not valid"})
        return None, meta_value

    last_year_reduction = (-last_reporting_year_ghg / preceding_year_ghg + 1) * 100
    result = round(last_year_reduction / float(fl_red), 2)

    meta_value.update(
        {
            "last_reporting_year": last_reporting_year,
            "last_reporting_year_ghg": last_reporting_year_ghg,
            "preceding_year_ghg": preceding_year_ghg,
            "last_year_reduction": f"{float(last_year_reduction):.2f}",
            "forward_looking_reduction": f"{float(fl_red):.2f}",
        }
    )

    return result, meta_value


def map_rating_to_score_8and9(obj_instance):

    if not obj_instance.is_float(obj_instance.company_score.rating_value):
        return 0.0
    if float(obj_instance.company_score.rating_value) >= 0.95:
        return obj_instance.max_score

    return 0.0
