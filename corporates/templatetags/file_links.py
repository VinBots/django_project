from django import template

register = template.Library()

# this tag is calling another template for displaying files to be downloaded
@register.inclusion_tag("corporates/display_files.html")
def display_file_links(my_query, title=""):

    return {
        "records": my_query,
        "title": title,
    }
