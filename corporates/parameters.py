import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIR_TO_CORP_CHARTS_TEMPLATES = "templates/django_project/corporates/charts/html_exports/"

def get_path_to_bubble(filename):
    path = os.path.join(
        BASE_DIR,
        DIR_TO_CORP_CHARTS_TEMPLATES) + "bubble_intensity_"+ filename + ".html"

    #if os.path.exists(path):
    return path

