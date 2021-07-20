DIR_TO_CORP_CHARTS_TEMPLATES = "django_project/corporates/charts/html_exports/"

def get_path_to_bubble(filename):

    return DIR_TO_CORP_CHARTS_TEMPLATES + "bubble_intensity_"+ filename + ".html"