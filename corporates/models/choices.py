class Options:

    # Not Applicable selection
    NA = ""
    NA_string = "NA"

    FULL = "full"
    PARTLY = "partly"
    NOT_COVERED = "no"

    COVERAGE_OPTIONS = [
        (FULL, "Full coverage"),
        (PARTLY, "Partly Covered"),
        (NOT_COVERED, "Not Covered"),
    ]

    LIMITED = "limited"
    REASONABLE_LIMITED = "reasonable-limited"
    NO_ASSURANCE = "no"
    REASONABLE = "reasonable"

    ASSURANCE_TYPE_OPTIONS = [
        (LIMITED, "Limited"),
        (REASONABLE, "Reasonable"),
        (REASONABLE_LIMITED, "Mix of Reasonable and Limited"),
        (NO_ASSURANCE, "No Assurance"),
    ]

    YEAR_DEFAULT_GHG = 2021
    YEAR_DEFAULT_VERIFICATION = 2021
    YEAR_DEFAULT_TARGET = 2021
    YEAR_DEFAULT_CDP = 2021

    YEAR_CHOICES = [(str(year), str(year)) for year in range(1990, 2051, 1)]
    FUTURE_YEAR_CHOICES = [(str(year), str(year)) for year in range(2021, 2051, 1)]

    YES = "yes"
    NO = "no"

    YESNO = [
        (YES, "Yes"),
        (NO, "No"),
        (NA, NA_string),
    ]

    SBTI_SET1_5 = "sbti_set_1_5"
    SBTI_SETBLW2 = "sbti_set_blw_2"
    SBTI_SET2 = "sbti_set_2"
    SBTI_COMMITTED = "committed"

    SBTI_CHOICES = [
        (SBTI_SET1_5, "Targets Set 1.5°C"),
        (SBTI_SETBLW2, "Targets Set Well-below 2°C"),
        (SBTI_SET2, "Targets Set 2°C"),
        (SBTI_COMMITTED, "Committed"),
    ]
    NT_STATUS = "Near term - Target Status"

    NT_STATUS_OPTIONS = [
        ("Committed", "Committed"),
        ("Targets Set", "Targets Set"),
        ("No", "No"),
    ]

    NT_CLASSIFICATION = "Near term - Target Classification"
    NT_CLASSIFICATION_OPTIONS = [
        ("1.5°C", "1.5°C"),
        ("Well-below 2°C", "Well-below 2°C"),
        ("2°C", "2°C"),
        ("NA", "NA"),
    ]

    SCOPE1 = "s1"
    SCOPE2 = "s2"
    SCOPE3 = "s3"
    SCOPE12_LOC = "s1s2loc"
    SCOPE12_MKT = "s1s2mkt"
    SCOPE123_LOC = "s1s2s3loc"
    SCOPE123_MKT = "s1s2s3mkt"

    SCOPE12_BEST = "s1s2best"
    SCOPE3_BEST = "scope_3_best"

    SCOPE_OPTIONS = [
        (SCOPE1, "Scope 1 only"),
        (SCOPE2, "Scope 2 only"),
        (SCOPE3, "Scope 3 only"),
        (SCOPE12_LOC, "Scopes 1 and 2 (location-based)"),
        (SCOPE12_MKT, "Scopes 1 and 2 (market-based)"),
        (SCOPE123_LOC, "Scopes 1, 2 (location-based) and 3"),
        (SCOPE123_MKT, "Scopes 1, 2 (market-based) and 3"),
    ]

    GROSS_ABSOLUTE = "gross_abs"
    FIXED_LEVEL = "fixed_level"
    NET_ABSOLUTE = "net_abs"
    GROSS_INTENSITY = "gross_int"
    NET_ZERO = "net_zero"

    TARGET_TYPES_OPTIONS = [
        (GROSS_ABSOLUTE, "Gross emissions - absolute target vs. base year"),
        (FIXED_LEVEL, "Gross emissions - absolute target without base year"),
        (NET_ABSOLUTE, "Net emissions - absolute target"),
        (GROSS_INTENSITY, "Gross emissions - intensity target"),
        (NET_ZERO, "Net Zero"),
    ]

    PUBLIC = "public"
    CDP = "cdp_2020"
    CDP_2021 = "cdp_2021"
    SBTI = "sbti"
    AGG = "aggregation"
    DISAG = "disaggregation"

    TARGET_SOURCES_OPTIONS = [
        (PUBLIC, "Public source"),
        (CDP, "CDP Climate Change Questionnaire"),
        (SBTI, "Science-Based Target Institute (SBTi)"),
        # (AGG, "Aggregation"),
        # (DISAG, "Disaggregation"),
    ]

    CDP_SCORE_OPTIONS = [
        ("a", "A"),
        ("a-", "A-"),
        ("b", "B"),
        ("b-", "B-"),
        ("c", "C"),
        ("c-", "C-"),
        ("d", "D"),
        ("d-", "D-"),
        ("f", "F"),
        ("not_scored", "Not Scored"),
        ("not_available", "Not Available"),
    ]
    CDP_SCORE_DEFAULT = "f"

    FINAL = "final"

    GHG_SOURCES_OPTIONS = [
        (PUBLIC, "Public source"),
        (CDP_2021, "2021 CDP Climate Change Questionnaire"),
        (CDP, "2020 CDP Climate Change Questionnaire"),
        (FINAL, "Final"),
    ]

    ACTUAL = "actual"
    TARGET = "target"
    BASELINE = "baseline"

    GHG_CATEGORY_OPTIONS = [
        (ACTUAL, "Actual"),
        (TARGET, "Target"),
        (BASELINE, "Baseline"),
    ]

    TARGET_DEFINITIONS = "Definitions"
    TOOLTIP_TEXT = "Both base year absolute emissions targets and fixed level targets \
        are absolute targets. An absolute target refers to the total amount of emissions being \
        emitted. A base year absolute emissions target refers to a target that aims to reduce \
        GHG emissions by a set amount relative to a base year. For example, an emissions\
        target aiming to reduce emissions by 50% by 2030. A fixed level target represents\
        a reduction in emissions to an absolute emissions level by a target year and is not\
        expressed relative to a base year. For example, an emissions target aiming to reach \
        100,000 tonnes CO2e by 2030. Net zero targets are a common type of fixed level goal, \
        for example: “to reach net zero emissions by 2050”. A base year emissions intensity \
        target aims to reduce a city’s emissions intensity (typically per GDP or per capita)\
        by a set amount relative to a base year. For example, an emissions target aiming to \
        reduce emissions per capita by 50% by 2030. This allows a city to set emissions reduction \
        targets while accounting for economic or population growth. A baseline scenario (business \
        as usual) target is a commitment to reduce emissions by a specified quantity relative \
        to a projected emissions baseline scenario, also referred to as a business as usual scenario.\
        A baseline scenario is a reference case that represents future events or conditions most \
        likely to occur in the absence of activities taken to meet the mitigation goal. \
        For example, a 50% reduction from baseline scenario emissions in 2030."

    # TOTAL CO2 ESTIMATES

    AS_REPORTED = "as_reported"

    S3_PRECEDING_YEAR = "scope_3_preceding_year"
    PRECEDING_YEAR_INTENSITY = "prec_year_intensity"
    RECENT_YEAR_INTENSITY = "recent_year_intensity"

    S3_SECTOR_INTENSITY_MANUAL = "s3_sector_intensity_manual"
    S3_SECTOR_INTENSITY_CALC = "s3_sector_intensity_calculated"

    SECTOR_INTENSITY_MANUAL = "sector_intensity_manual"
    SECTOR_INTENSITY_CALC = "sector_intensity_calculated"

    CO2_ESTIMATES_METHODS = [
        AS_REPORTED,
        S3_PRECEDING_YEAR,
        PRECEDING_YEAR_INTENSITY,
        RECENT_YEAR_INTENSITY,
        S3_SECTOR_INTENSITY_MANUAL,
        S3_SECTOR_INTENSITY_CALC,
        SECTOR_INTENSITY_MANUAL,
        SECTOR_INTENSITY_CALC,
    ]
    CO2_ESTIMATES_METHODS_DESCRIPTION = {
        AS_REPORTED: "As reported",
        S3_PRECEDING_YEAR: "Scope 3 based on previous year",
        PRECEDING_YEAR_INTENSITY: "Previous year intensity (revenue)",
        RECENT_YEAR_INTENSITY: "Recent intensity (revenue)",
        S3_SECTOR_INTENSITY_MANUAL: "Scope 3 based on pre-defined sector intensity (revenue)",
        S3_SECTOR_INTENSITY_CALC: "Scope 3 based on pre-calculated sector intensity (revenue)",
        SECTOR_INTENSITY_MANUAL: "Pre-defined sector intensity (revenue)",
        SECTOR_INTENSITY_CALC: "Pre-calculated sector intensity (revenue)",
    }

    DEFAULT_DOCUMENT = "sustainability_report"
    PROGRESS_DOCUMENT = "progress_report"
    TCFD_DOCUMENT = "tcfd_report"
    CLIMATE_PLAN = "climate_plan"

    DOCUMENT_CHOICES = [
        (DEFAULT_DOCUMENT, "Sustainability Report"),
        (TCFD_DOCUMENT, "TCFD Report"),
        (PROGRESS_DOCUMENT, "Progress Report"),
        (CLIMATE_PLAN, "Climate Plan"),
    ]

    NEW = "new"
    UNDERWAY = "underway"
    ACHIEVED = "achieved"
    EXPIRED = "expired"
    REVISED = "revised"
    REPLACED = "replaced"
    RETIRED = "retired"

    ACTIVE_TARGET_STATUS = [
        NEW,
        ACHIEVED,
        REVISED,
    ]

    TARGET_STATUS = [
        (NEW, "New"),
        (UNDERWAY, "Underway"),
        (ACHIEVED, "Achieved"),
        (EXPIRED, "Expired"),
        (REVISED, "Revised"),
        (REPLACED, "Replaced"),
        (RETIRED, "Retired"),
    ]

    CDP_OVERRIDE_CHOICES = [
        (True, "Yes"),
        (False, "No"),
    ]
