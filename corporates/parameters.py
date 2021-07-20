import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_TEMPLATE = os.path.join(BASE_DIR, 'templates', 'django_project')
DIR_TO_CORP_CHARTS_TEMPLATES = "django_project/corporates/charts/html_exports/"

def get_path_to_bubble(filename):
    path = os.path.join(
        DIR_TEMPLATE,
        DIR_TO_CORP_CHARTS_TEMPLATES) + "bubble_intensity_"+ filename + ".html"

    if os.path.exists(path):
        return path

