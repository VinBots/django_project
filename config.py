import json


def load_json(filename):
    with open(filename) as f:
        return json.load(f)


class FieldsName:
    COMPANY_ID = "company_id"
    SOURCE = "source"
    TARGET_TYPE = "target_type"
    REPORTING_YEAR = "reporting_year"
    LAST_REPORTING_YEAR = "last_reporting_year"


class TargetsType:
    FIELD = "target_type"
    NET0_POLICY = "net_zero_policy"
    NET_ABSOLUTE = "net_abs"
    GROSS_ABSOLUTE = "gross_abs"


class TargetsSources:
    FIELD = "source"
    SBTI = "sbti"
    PUBLIC = "public"
    CDP = "cdp"


class Targets:
    TYPE = TargetsType
    REDUCTION_OBJ = "reduction_obj"
    SOURCES = TargetsSources
    SCOPE = "scope"
    COV_S3 = "cov_s3"
    BASE_YEAR = "base_year"
    TARGET_YEAR = "target_year"


class GhgDataSources:
    FIELD = "Source"
    FINAL = "Final"


class GHG:
    SOURCES = GhgDataSources
    SCOPE1 = "ghg_scope_1"
    SCOPE2_LOC = "ghg_loc_scope_2"
    SCOPE2_MKT = "ghg_mkt_scope_2"
    SCOPE3 = "ghg_scope3_total"
    TOTAL = "ghg_total"


class Scores:
    TRANSPARENCY = "transp_score"
    COMMITMENTS = "comm_score"
    ACTIONS = "actions_score"
    TRANSPARENCY_RATIO = "transp_ratio"
    COMMITMENTS_RATIO = "comm_ratio"
    ACTIONS_RATIO = "actions_ratio"
    CATEGORIES = [TRANSPARENCY, COMMITMENTS, ACTIONS]
    TOTAL = "score"
    RANK = "rank"
    STRUCTURE = load_json("/home/django/django_project/score_structure.json")
    PCT_FIELDS = [
        "rat_6_1",
        "rat_6_2",
        "rat_8_1_meta_1",
        "rat_8_1_meta_2",
        "rat_8_2_meta_1",
        "rat_8_2_meta_2",
        "rat_9_1_meta_1",
        "rat_9_1_meta_2",
        "rat_9_2_meta_1",
        "rat_9_2_meta_2",
    ]


class Library:
    
    LIST_CSV = "library_db"
    FOLDER = "reports"
    SUB_FOLDER_NAME = "folder_name"
    FILENAME = "filename"
    DESC = "desc"
    YEAR = "year"
    PART = "part"
    SUST_REPORT = "sust_report"
    GHG = "ghg"
    TARGETS = "targets"
    VERIFICATION = "verification"
    CATEGORIES_NAME = [SUST_REPORT, GHG, TARGETS, VERIFICATION]
    CATEGORIES_DESC = {
        SUST_REPORT: "Sustainability Reporting",
        GHG: "GHG data",
        TARGETS: "Targets reporting",
        VERIFICATION: "Verification",
    }


class DataFromXlsx:
    GHG_QUANT = "ghg_quant"
    CORP_SCORES = "corp_scores"
    SCORES_SUMMARY = "score_summary"
    TARGETS_QUANT = "targets_quant"
    SCORES_DETAILS = "score_details"
    REPORTING = "reporting"



class Config:
    DATA_FOLDER = "/home/django/net0_docs"
    XLS_FOLDER = "excel_db"
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"
    LIBRARY = Library
    FIELDS = FieldsName
    SCORES = Scores
    TARGETS = Targets
    GHG = GHG
    DATA_FROM_XLSX = DataFromXlsx
    SBTI_XLSX = "/home/django/scripts/data/companies-taking-action.xlsx"
    SBTI_CSV = "/home/django/scripts/data/sbti_data.csv"
    COMPANIES_CSV = f"{DATA_FOLDER}/{XLS_FOLDER}/companies.csv"
