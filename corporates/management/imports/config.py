import corporates
from corporates.models.choices import Options


def to_int(text):
    if text in ["NR", "NA", ""]:
        return 0
    return int(float(text))


def to_int_or_none(text):
    try:
        return int(float(text))
    except:
        return None


def yes_to_true(text):
    if text == "yes":
        return True
    else:
        return False


def lowercase(text):
    if text:
        return text.lower()


def ghg_quant_source(text):
    mapping_dict = {
        "Public": "public",
        "CDP": "cdp",
        "cdp_2021": "cdp_2021",
        "Final": "final",
    }

    return mapping_dict.get(text, "")


def target_coverage(text):
    if text == "1":
        return "full"
    elif text == "NR" or text == "0":
        return "no"
    return text


def target_cov_s3(text):
    mapping_dict = {"full": "full", "no": "no", "NR": "no", "partly": "partly"}
    return mapping_dict.get(text, "")


def to_float(text):
    if text in ["NA", ""]:
        return None
    elif text[-1] == "%":
        return float(text[:-1])
    else:
        return float(text) * 100


def scope_coverage_tf(text):
    mapping_dict = {
        "S1": Options.SCOPE1,
        "S2": Options.SCOPE2,
        "S3": Options.SCOPE3,
        "S1S2loc": Options.SCOPE12_LOC,
        "S1S2mkt": Options.SCOPE12_MKT,
        "S1S2S3loc": Options.SCOPE123_LOC,
        "S1S2S3mkt": Options.SCOPE123_MKT,
    }

    return mapping_dict.get(text, "other")


def year_format_tf(text):
    if text:
        return str(int(float(text)))
    else:
        return None


def target_type_tf(text):

    valid_targets = [valid_target for valid_target, _ in Options.TARGET_TYPES_OPTIONS]

    if text not in valid_targets:
        return None
    else:
        return text


# def map_sbti_status (text):
#     mapping_dict = {"Committed": "committed", "Targets Set": "no", "NR": "no", "partly": "partly"}
#     return mapping_dict.get(text, "")


def map_sbti_classification(text):
    pass


def sp100(text):
    if int(float(text)) == 1:
        return "SP100"
    else:
        return "SP500"


cols_to_fetch_benchmark = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "SP100": {
        "fk": True,
        "fk_model": corporates.models.grouping.Benchmark,
        "fk_field": "name",
        "model_field": "primary_benchmark",
        "map": True,
        "mapping": sp100,
    },
    "sub_industry_name": {
        "fk": True,
        "fk_model": corporates.models.grouping.GICS,
        "fk_field": "sub_industry_name",
        "model_field": "gics_sub_industry_name",
        "map": False,
        "mapping": {},
    },
}


cols_to_fetch_score_desc = {
    "name": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "name",
        "map": False,
        "mapping": "",
    },
    "description": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "description",
        "map": False,
        "mapping": "",
    },
    "max_score": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "max_score",
        "map": False,
        "mapping": "",
    },
    "rating_description": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "rating_description",
        "map": False,
        "mapping": "",
    },
}

cols_to_fetch_msci = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "rat_10_1": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "ITR",
        "map": False,
        "mapping": "",
    },
}


cols_to_fetch_sbti = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "sbti_status": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "status",
        "map": False,
        "mapping": "",
    },
    "sbti_classification": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "classification",
        "map": False,
        "mapping": "",
    },
}

cols_to_fetch_net_zero = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "stated": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "stated",
        "map": False,
        "mapping": "",
    },
    "coverage": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "coverage",
        "map": True,
        "mapping": scope_coverage_tf,
    },
    "scope_3_coverage": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope_3_coverage",
        "map": True,
        "mapping": target_cov_s3,
    },
    "target_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "target_year",
        "map": True,
        "mapping": year_format_tf,
    },
    "already_reached": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "already_reached",
        "map": False,
        "mapping": "",
    },
    "ongoing": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "ongoing",
        "map": False,
        "mapping": "",
    },
    "ongoing_coverage": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "ongoing_coverage",
        "map": True,
        "mapping": scope_coverage_tf,
    },
    "ongoing_scope_3_coverage": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "ongoing_scope_3_coverage",
        "map": True,
        "mapping": target_cov_s3,
    },
    "year_since": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "year_since",
        "map": True,
        "mapping": year_format_tf,
    },
}

cols_to_fetch_targets_quant = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "target_type": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "type",
        "map": True,
        "mapping": target_type_tf,
    },
    "source": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "source",
        "map": False,
        "mapping": "",
    },
    "scope_v2": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope_coverage",
        "map": True,
        "mapping": scope_coverage_tf,
    },
    "cov_s3": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope_3_coverage",
        "map": True,
        "mapping": target_cov_s3,
    },
    "reduction_obj": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "reduction_obj",
        "map": True,
        "mapping": to_float,
    },
    "base_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "base_year",
        "map": True,
        "mapping": year_format_tf,
    },
    "baseline": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "baseline",
        "map": True,
        "mapping": to_int,
    },
    "target_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "target_year",
        "map": True,
        "mapping": year_format_tf,
    },
    "start_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "start_year",
        "map": True,
        "mapping": year_format_tf,
    },
}


cols_to_fetch_verification = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "scope12_2_years": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope12_reporting_2_years",
        "map": False,
        "mapping": "",
    },
    "scope12_completeness": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope12_reporting_completeness",
        "map": False,
        "mapping": "",
    },
    "scope12_verification": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope12_verification_completeness",
        "map": False,
        "mapping": "",
    },
    "assurance_type": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope12_assurance_type",
        "map": False,
        "mapping": "",
    },
    "scope3_completeness": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope3_reporting_completeness",
        "map": False,
        "mapping": "",
    },
    "scope3_verification": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope3_verification_completeness",
        "map": False,
        "mapping": "",
    },
    "assurance_type": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "scope3_assurance_type",
        "map": False,
        "mapping": "",
    },
    "last_reporting_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "reporting_year",
        "map": False,
        "mapping": "",
    },
}


cols_to_fetch_ghg_quant = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "reporting_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "reporting_year",
        "map": True,
        "mapping": year_format_tf,
    },
    "Source": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "source",
        "map": True,
        "mapping": ghg_quant_source,
    },
}

GHG_FIELDS = [
    "ghg_scope_1",
    "ghg_loc_scope_2",
    "ghg_mkt_scope_2",
    # "ghg_scope3_total",
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
    "ghg_other_downstream_scope3",
    "ghg_other_upstream_scope3",
]
for each_ghg_field in GHG_FIELDS:
    cols_to_fetch_ghg_quant.update(
        {
            each_ghg_field: {
                "fk": False,
                "fk_model": "",
                "fk_field": "",
                "model_field": each_ghg_field,
                "map": True,
                "mapping": to_int_or_none,
            }
        }
    )


cols_to_fetch_ghg_qual = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "cdp_report_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "reporting_year",
        "map": False,
        "mapping": "",
    },
    "cdp_report_public": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "made_public",
        "map": True,
        "mapping": yes_to_true,
    },
    "cdp_score_year": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "questionnaire_year",
        "map": True,
        "mapping": year_format_tf,
    },
    "cdp_score": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "score",
        "map": True,
        "mapping": lowercase,
    },
    "reviewer_comment": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "comments",
        "map": False,
        "mapping": {},
    },
}

cols_to_fetch_corporates = {
    "company_id": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "company_id",
        "map": True,
        "mapping": to_int,
    },
    "company_name": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "name",
        "map": False,
        "mapping": {},
    },
    "short_name": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "short_name",
        "map": False,
        "mapping": {},
    },
    "link": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "web_URL",
        "map": False,
        "mapping": {},
    },
}


cols_to_fetch_matching = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "tradingview_exch_symb": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "tradingview_symbol",
        "map": False,
        "mapping": {},
    },
    "sbti_company_name": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "sbti_company_name",
        "map": False,
        "mapping": {},
    },
}

cols_to_fetch_finnhub = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "finnhub_symb": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "symbol",
        "map": False,
        "mapping": {},
    },
    "finnhub_name": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "name",
        "map": False,
        "mapping": {},
    },
}

cols_to_fetch_grouping_cat = {
    "sector": {
        "fk": False,
        "fk_model": "",
        "fk_field": "",
        "model_field": "name",
        "map": False,
        "mapping": {},
    },
}

cols_to_fetch_grouping = {
    "company_id": {
        "fk": True,
        "fk_model": corporates.models.Corporate,
        "fk_field": "company_id",
        "model_field": "company",
        "map": True,
        "mapping": to_int,
    },
    "Sector1": {
        "fk": True,
        "fk_model": corporates.models.grouping.GICS,
        "fk_field": "name",
        "model_field": "primary_sector",
        "map": False,
        "mapping": {},
    },
}

# this dictionary is defining for each csv file which model will be used and which data (columns) will be migrated
# migrated data is defined in "cols_to_fetch"
# the model is defined in "Model_to_Use"
# add_arg is a boolean that adds a value for submitter in the model. The model must contain a field called "submitter"


csv_file_mapping = {
    "companies.csv": {
        "cols_to_fetch": [
            cols_to_fetch_corporates,
            cols_to_fetch_benchmark,
            cols_to_fetch_matching,
            cols_to_fetch_finnhub,
        ],
        "Model_to_Use": [
            corporates.models.Corporate,
            corporates.models.CorporateGrouping,
            corporates.models.Matching,
            corporates.models.FinnhubMatching,
        ],
        "add_arg": [False, False, False, False],
    },
    # "grouping.csv": {
    #     "cols_to_fetch": [cols_to_fetch_grouping],
    #     "Model_to_Use": [corporates.models.CorporateGrouping],
    #     "add_arg": [False],
    # },
    "score_desc.csv": {
        "cols_to_fetch": [cols_to_fetch_score_desc],
        "Model_to_Use": [corporates.models.Score],
        "add_arg": [False],
    },
    "ghg_qual.csv": {
        "cols_to_fetch": [cols_to_fetch_ghg_qual, cols_to_fetch_verification],
        "Model_to_Use": [corporates.models.CDP, corporates.models.Verification],
        "add_arg": [True, True],
    },
    "ghg_quant.csv": {
        "cols_to_fetch": [cols_to_fetch_ghg_quant],
        "Model_to_Use": [corporates.models.GHGQuant],
        "add_arg": [True],
    },
    "targets_quant.csv": {
        "cols_to_fetch": [cols_to_fetch_targets_quant],
        "Model_to_Use": [corporates.models.TargetQuant],
        "add_arg": [True],
    },
    "net_zero_details.csv": {
        "cols_to_fetch": [cols_to_fetch_net_zero],
        "Model_to_Use": [corporates.models.NetZero],
        "add_arg": [True],
    },
    "score_details.csv": {
        "cols_to_fetch": [cols_to_fetch_sbti, cols_to_fetch_msci],
        "Model_to_Use": [corporates.models.SBTI, corporates.models.MSCI],
        "add_arg": [False, False],
    },
    "new_input.csv": {
        "cols_to_fetch": [cols_to_fetch_ghg_quant],
        "Model_to_Use": [corporates.models.GHGQuant],
        "add_arg": [True],
    },
}
