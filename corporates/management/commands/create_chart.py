from django.core.management import BaseCommand

from corporates.models import Corporate
from corporates.management.charts import charts_gen
from corporates.management.charts import ghg_scope3_pie_chart, bubble_charts


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):

        company_id_list = Corporate.objects.values_list("company_id", flat=True)
        # company_id_list = [14]
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
