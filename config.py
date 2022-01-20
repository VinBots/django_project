import json
from pydantic import Field, BaseModel
from typing import Optional


def load_json(filename):
    with open(filename) as f:
        return json.load(f)


class FieldsName:
    COMPANY_ID = "company_id"
    COMPANY_NAME = "company_name"
    COMPANY_ISIN = "ISIN"
    SOURCE = "source"
    TARGET_TYPE = "target_type"
    REPORTING_YEAR = "reporting_year"
    LAST_REPORTING_YEAR = "last_reporting_year"


class TargetsType:
    FIELD = "target_type"
    NET0_POLICY = "net_zero_policy"
    NET_ABSOLUTE = "net_abs"
    GROSS_ABSOLUTE = "gross_abs"


class SBTI:
    FIELD = "sbti"
    NT_STATUS = "Near term - Target Status"
    NT_CLASSIFICATION = "Near term - Target Classification"


class TargetsSources:
    FIELD = "source"
    SBTI = SBTI
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


class ScoreBreakdown:

    RAT1_1 = {
        "type": "rating",
        "name": "rat_1_1",
        "children": None,
        "score": {"name": "sco_1_1", "value": 0},
        "rating": {"name": "rat_1_1", "value": 0},
    }
    RAT1_2 = {
        "type": "rating",
        "name": "rat_1_2",
        "children": None,
        "score": {"name": "sco_1_2", "value": 0},
        "rating": {"name": "rat_1_2", "value": 0},
    }
    RAT2_1 = {
        "type": "rating",
        "name": "rat_2_1",
        "children": None,
        "score": {"name": "sco_2_1", "value": 0},
        "rating": {"name": "rat_2_1", "value": 0},
    }
    RAT2_2 = {
        "type": "rating",
        "name": "rat_2_2",
        "children": None,
        "score": {"name": "sco_2_2", "value": 0},
        "rating": {"name": "rat_2_2", "value": 0},
    }
    RAT3_1 = {
        "type": "rating",
        "name": "rat_3_1",
        "children": None,
        "score": {"name": "sco_3_1", "value": 0},
        "rating": {"name": "rat_3_1", "value": 0},
    }
    RAT3_2 = {
        "type": "rating",
        "name": "rat_3_2",
        "children": None,
        "score": {"name": "sco_3_2", "value": 0},
        "rating": {"name": "rat_3_2", "value": 0},
    }
    RAT4_1 = {
        "type": "rating",
        "name": "rat_4_1",
        "children": None,
        "score": {"name": "sco_4_1", "value": 0},
        "rating": {"name": "rat_4_1", "value": 0},
    }
    RAT4_2 = {
        "type": "rating",
        "name": "rat_4_2",
        "children": None,
        "score": {"name": "sco_4_2", "value": 0},
        "rating": {"name": "rat_4_2", "value": 0},
    }
    RAT4_3 = {
        "type": "rating",
        "name": "rat_4_3",
        "children": None,
        "score": {"name": "sco_4_3", "value": 0},
        "rating": {"name": "rat_4_3", "value": 0},
    }
    RAT5_1 = {
        "type": "rating",
        "name": "rat_5_1",
        "children": None,
        "score": {"name": "sco_5_1", "value": 0},
        "rating": {"name": "rat_5_1", "value": 0},
    }
    RAT5_2 = {
        "type": "rating",
        "name": "rat_5_2",
        "children": None,
        "score": {"name": "sco_5_2", "value": 0},
        "rating": {"name": "rat_5_2", "value": 0},
    }
    RAT6_1 = {
        "type": "rating",
        "name": "rat_6_1",
        "children": None,
        "score": {"name": "sco_6_1", "value": 0},
        "rating": {"name": "rat_6_1", "value": 0},
    }
    RAT6_2 = {
        "type": "rating",
        "name": "rat_6_2",
        "children": None,
        "score": {"name": "sco_6_2", "value": 0},
        "rating": {"name": "rat_6_2", "value": 0},
    }
    RAT7_1 = {
        "type": "rating",
        "name": "rat_7_1",
        "children": None,
        "score": {"name": "sco_7_1", "value": 0},
        "rating": {"name": "rat_7_1", "value": 0},
    }
    RAT8_1 = {
        "type": "rating",
        "name": "rat_8_1",
        "children": None,
        "score": {"name": "sco_8_1", "value": 0},
        "rating": {"name": "rat_8_1", "value": 0},
    }
    RAT8_2 = {
        "type": "rating",
        "name": "rat_8_2",
        "children": None,
        "score": {"name": "sco_8_2", "value": 0},
        "rating": {"name": "rat_8_2", "value": 0},
    }
    RAT9_1 = {
        "type": "rating",
        "name": "rat_9_1",
        "children": None,
        "score": {"name": "sco_9_1", "value": 0},
        "rating": {"name": "rat_9_1", "value": 0},
    }
    RAT9_2 = {
        "type": "rating",
        "name": "rat_9_2",
        "children": None,
        "score": {"name": "sco_9_2", "value": 0},
        "rating": {"name": "rat_9_2", "value": 0},
    }
    RAT10_1 = {
        "type": "rating",
        "name": "rat_10_1",
        "children": None,
        "score": {"name": "sco_10_1", "value": 0},
        "rating": {"name": "rat_10_1", "value": 0},
    }
    RAT10_2 = {
        "type": "rating",
        "name": "rat_10_2",
        "children": None,
        "score": {"name": "sco_10_2", "value": 0},
        "rating": {"name": "rat_10_2", "value": 0},
    }

    PRINC_1 = {"type": "aggr", "name": "princ_score_1", "children": [RAT1_1, RAT1_2]}
    PRINC_2 = {"type": "aggr", "name": "princ_score_2", "children": [RAT2_1, RAT2_2]}
    PRINC_3 = {"type": "aggr", "name": "princ_score_3", "children": [RAT3_1, RAT3_2]}
    PRINC_4 = {
        "type": "aggr",
        "name": "princ_score_4",
        "children": [RAT4_1, RAT4_2, RAT4_3],
    }
    PRINC_5 = {"type": "aggr", "name": "princ_score_5", "children": [RAT5_1, RAT5_2]}
    PRINC_6 = {"type": "aggr", "name": "princ_score_6", "children": [RAT6_1, RAT6_2]}
    PRINC_7 = {"type": "aggr", "name": "princ_score_7", "children": [RAT7_1]}
    PRINC_8 = {"type": "aggr", "name": "princ_score_8", "children": [RAT8_1, RAT8_2]}
    PRINC_9 = {"type": "aggr", "name": "princ_score_9", "children": [RAT9_1, RAT9_2]}
    PRINC_10 = {
        "type": "aggr",
        "name": "princ_score_10",
        "children": [RAT10_1, RAT10_2],
    }

    CAT1 = {
        "type": "aggr",
        "name": "transp_score",
        "children": [PRINC_1, PRINC_2, PRINC_3],
    }
    CAT2 = {
        "type": "aggr",
        "name": "comm_score",
        "children": [PRINC_4, PRINC_5, PRINC_6, PRINC_7],
    }
    CAT3 = {
        "type": "aggr",
        "name": "actions_score",
        "children": [PRINC_8, PRINC_9, PRINC_10],
    }
    TOTAL_SCORE = {
        "type": "aggr",
        "name": "total_score",
        "children": [CAT1, CAT2, CAT3],
    }


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
    BREAKDOWN = ScoreBreakdown
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


class Company(BaseModel):

    company_name: str
    company_id: int
    sbti_nt_status: Optional[str]
    sbti_nt_classification: Optional[str]
    # isic: str
    # ghg_s1s2: float
    # ghg_s3: float

    # country: Optional[str]
    # region: Optional[str]
    # sector: Optional[str]
    # industry_level_1: Optional[str]
    # industry_level_2: Optional[str]
    # industry_level_3: Optional[str]
    # industry_level_4: Optional[str]

    # company_revenue: Optional[float]
    # company_market_cap: Optional[float]
    # company_enterprise_value: Optional[float]
    # company_total_assets: Optional[float]
    # company_cash_equivalents: Optional[float]


class FilesPath:

    DATA_FOLDER = "/home/django/net0_docs"
    XLS_FOLDER = "excel_db"
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"

    ORIGINAL_XLSX = "/home/django/net0_docs/excel_db/original/sp100.xlsx"
    SBTI_XLSX = "/home/django/server/data/input_data/companies-taking-action.xlsx"
    SBTI_CSV = "/home/django/scripts/data/sbti_data.csv"
    COMPANIES_CSV = f"{DATA_FOLDER}/{XLS_FOLDER}/companies.csv"


class Config:

    DATA_FOLDER = "/home/django/net0_docs"
    XLS_FOLDER = "excel_db"
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"

    ORIGINAL_XLSX = "/home/django/net0_docs/excel_db/original/sp100.xlsx"
    SBTI_XLSX = "/home/django/server/data/companies-taking-action.xlsx"
    SBTI_CSV = "/home/django/scripts/data/sbti_data.csv"
    COMPANIES_CSV = f"{DATA_FOLDER}/{XLS_FOLDER}/companies.csv"

    LIBRARY = Library
    FIELDS = FieldsName
    SCORES = Scores
    TARGETS = Targets
    GHG = GHG
    DATA_FROM_XLSX = DataFromXlsx
    COMPANY = Company
    FILES_PATH = FilesPath
