from corporates.models import TargetQuant
from corporates.models.choices import Options
from corporates.management.commands.base_scores.score_utilities import (
    get_forward_looking_target,
)


def get_valid_target(score_value, valid_target):

    queryset = TargetQuant.objects.get_earliest_highest(
        company_id=score_value.company.company_id,
        valid_target=valid_target,
    )
    if not queryset.exists():
        meta_value = {"error": f"No target found for {valid_target}"}
        return None, meta_value

    return queryset[0], {}


def get_rating_6_x(score_value, valid_target=None):

    meta_value = {}

    # step 1: Get a valid target
    selected_target, meta_value = get_valid_target(
        score_value, valid_target=valid_target
    )
    if not selected_target:
        return None, meta_value

    # Step 2: Get the baseline of the selected target
    # Step 2.1" Update the auto_baseline field by calculating the baseline
    # based on existing GHG Inventory
    selected_target.get_auto_baseline()

    # Step 2.1 if a baseline already exists, choose it.
    baseline = selected_target.get_baseline()
    if not baseline:
        meta_value.update(
            {
                "error_msg": f"No baseline for {selected_target.get_scope_coverage_display()} could be found"
            }
        )
        return None, meta_value

    # Step 3: Calculate the forward looking reduction target of the selected target
    fl_red, meta_msg = get_forward_looking_target(
        company_id=score_value.company.company_id,
        selected_target=selected_target,
        baseline=baseline,
    )
    meta_value.update(meta_msg)

    if not fl_red:
        return None, meta_value

    meta_value.update(
        {
            "baseline": baseline,
            "reduction_obj": f"{float(selected_target.reduction_obj):.2f}",
            "target_year": selected_target.target_year,
        }
    )
    return fl_red, meta_value


def map_rating_6_x_to_score(obj_instance):

    if (
        not obj_instance.is_float(obj_instance.company_score.rating_value)
        or float(obj_instance.company_score.rating_value) <= 0
    ):
        return 0
    result = min(
        [
            float(obj_instance.company_score.rating_value)
            / obj_instance.MAX_REDUCTION_6_x,
            1.0,
        ]
    )

    return result * obj_instance.max_score
