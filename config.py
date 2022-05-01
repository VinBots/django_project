import os
from django.conf import settings


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


class FilesPath:

    XLS_FOLDER = "excel_db"
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"

    ORIGINAL_XLSX = os.path.join(
        settings.SERVER_BASE_DIR, "net0_docs/excel_db/original/sp100.xlsx"
    )  # "/home/django/net0_docs/excel_db/original/sp100.xlsx"
    SBTI_XLSX = os.path.join(
        settings.SERVER_BASE_DIR, "server/data/input_data/companies-taking-action.xlsx"
    )  # "/home/django/server/data/input_data/companies-taking-action.xlsx"
    SBTI_CSV = os.path.join(
        settings.SERVER_BASE_DIR, "scripts/data/sbti_data.csv"
    )  # "/home/django/scripts/data/sbti_data.csv"
    COMPANIES_CSV = f"{settings.DATA_FOLDER}/{XLS_FOLDER}/companies.csv"


class Config:

    DATA_FOLDER = os.path.join(
        settings.SERVER_BASE_DIR, "net0_docs"
    )  # "/home/django/net0_docs"
    XLS_FOLDER = "excel_db"
    TOP_STATS_FILE = "stats/general_stats.json"
    LIBRARY_FOLDER = "reports"

    ORIGINAL_XLSX = os.path.join(
        settings.SERVER_BASE_DIR, "net0_docs/excel_db/original/sp100.xlsx"
    )  # "/home/django/net0_docs/excel_db/original/sp100.xlsx"
    SBTI_XLSX = os.path.join(
        settings.SERVER_BASE_DIR, "server/data/companies-taking-action.xlsx"
    )  # /home/django/server/data/companies-taking-action.xlsx"
    SBTI_CSV = os.path.join(
        settings.SERVER_BASE_DIR, "sbti_data.csv"
    )  # "/home/django/scripts/data/sbti_data.csv"
    COMPANIES_CSV = f"{DATA_FOLDER}/{XLS_FOLDER}/companies.csv"

    LIBRARY = Library
    FILES_PATH = FilesPath
