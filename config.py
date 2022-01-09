import json


def load_json(filename):
    with open (filename) as f:
        return json.load(f)

class FieldsName:
    COMPANY_ID = "company_id"
    SOURCE = 'source'
    TARGET_TYPE = "target_type"
    REPORTING_YEAR = "reporting_year"

class TargetsType:
    NET0_POLICY = "net_zero_policy"
    NET_ABSOLUTE = "net_abs"
    GROSS_ABSOLUTE = "gross_abs"

class TargetsSources:
    SBTI = "sbti"
    PUBLIC = "public"
    CDP = "cdp"

class Targets:
    TYPE = TargetsType
    REDUCTION_OBJ = "reduction_obj"
    SOURCES = TargetsSources

class GhgDataSources:
    FINAL = "Final"

class GHG:
    SOURCES = GhgDataSources
    SCOPE1 = 'ghg_scope_1'
    SCOPE2_LOC = 'ghg_loc_scope_2'
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
    STRUCTURE = load_json('score_structure.json')
 
class Config:
    DATA_FOLDER = "/home/django/net0_docs"
    XLS_FOLDER = 'excel_db'
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"
    FIELDS = FieldsName
    SCORES = Scores
    TARGETS = Targets
    GHG = GHG
