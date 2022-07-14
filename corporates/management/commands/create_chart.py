from django.core.management import BaseCommand

from corporates.management.charts import charts_gen
from corporates.management.charts import ghg_scope3_pie_chart, bubble_charts
from corporates.management.utilities import parse_extract


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-company_id", type=int)

    def handle(self, *args, **options):

        arg_dict = parse_extract(options)
        company_id_list = arg_dict.get("company_id_list")

        create_chart_func(company_id_list)


def create_chart_func(company_id_list):

    chart_types = [
        {
            "name": "ghg_pie_chart",
            "generator": ghg_scope3_pie_chart.ghg_scope3_pie_chart_from_db,
            "params": {},
        },
        {
            "name": "bubble",
            "generator": bubble_charts.bubble_chart_from_db,
            "params": {},
        },
    ]
    for company_id in company_id_list:
        for chart_type in chart_types:
            new_chart = charts_gen.Charts(chart_type, company_id)
            new_chart.build_save()
