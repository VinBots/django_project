class FIELDS_NAME:
    COMPANY_ID = "company_id"   
    SOURCE = 'source'
    TARGET_TYPE =  "target_type"
    REPORTING_YEAR = "reporting_year"

class SCORES:
    TRANSPARENCY = "transp_score"
    COMMITMENTS = "comm_score"
    ACTIONS = "actions_score"
    TOTAL = "score"
    RANK =  "rank"

class TARGETS_TYPE:
    NET0_POLICY = "net_zero_policy"
    NET_ABSOLUTE = "net_abs"
    GROSS_ABSOLUTE = "gross_abs"

class TARGETS_SOURCES:
    SBTI = "sbti"
    PUBLIC = "public"
    CDP = "cdp"

class TARGETS:
    TYPE = TARGETS_TYPE
    REDUCTION_OBJ = "reduction_obj"
    SOURCES = TARGETS_SOURCES

class GHG_DATA_SOURCES:
    FINAL = "Final"
    
class GHG:
    SOURCES = GHG_DATA_SOURCES
    SCOPE1 = 'ghg_scope_1'
    SCOPE2_LOC = 'ghg_loc_scope_2'
    SCOPE2_MKT = "ghg_mkt_scope_2"
    SCOPE3 = "ghg_scope3_total"
    TOTAL = "ghg_total"



class Config:
    DATA_FOLDER = "/home/django/net0_docs"
    XLS_FOLDER = 'excel_db'
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"
    FIELDS = FIELDS_NAME
    SCORES = SCORES
    TARGETS = TARGETS
    GHG = GHG

