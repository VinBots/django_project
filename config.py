import json


def load_json(filename):
    with open (filename) as f:
        return json.load(f).to_dict()

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
"""
class ScoreMethodology:
    PRINCIPLES_REF = [
        '1',
        '2',
        '3',
        '',
        '4',
        '5',
        '6',
        '7',
        '',
        '8',
        '9',
        '10',
        '',
    ]
    PRINCIPLES_DESC = [
        'At least 2 years of GHG emissions for scope 1 and 2 are publicly-available and externally-verified',
        'Scope 3 emissions are fully reported and externally-verified',
        'CDP score and interim reporting demonstrate the highest level of transparency',
        '',
        'Net Zero Commitments by 2050 include an intermediate target and cover all the emissions',
        'Net Zero targets demonstrate a high-level of emergency',
        'Emission reduction targets on a forward-looking basis are ambitious',
        'Targets are science-based as validated by SBTi',
        '',
        'Results re. operational emissions reduction: on-pace (performance-to-date) and momentum (forward-looking targets)',
        'Results re. value chain emissions reduction: on-pace (performance-to-date) and momentum (forward-looking targets)',
        'Implied Temperature Rating by MSCi',
        '',
    ]
    MAX_SCORES = [
        '10',
        '10',
        '10',
        '30',
        '10',
        '10',
        '10',
        '10',
        '40',
        '10',
        '10',
        '10',
        '30',
    ]
"""

class Scores:
    TRANSPARENCY = "transp_score"
    COMMITMENTS = "comm_score"
    ACTIONS = "actions_score"
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
