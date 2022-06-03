# from chart_types import (
#     bubble_charts,
#     bullet_charts,
#     ghg_bar_charts,
#     ghg_scope3_pie_chart,
# )
import os
from plotly.offline import plot
from django.conf import settings

# CHART_TYPES = {
#     "bullet": {
#         "name": "bullet",
#         "generator": bullet_charts.bullet_chart_from_xls,
#         "params": {
#             "year": "2019",
#         },
#     },
#     "bubble": {
#         "name": "bubble",
#         "generator": bubble_charts.bubble_chart_from_xls,
#         "params": {
#             "year": "2019",
#         },
#     },
#     "ghg_bar": {
#         "name": "ghg_bar",
#         "generator": ghg_bar_charts.ghg_bar_chart_from_xls,
#         "params": {},
#     },
#     "ghg_pie_chart": {
#         "name": "ghg_pie_chart",
#         "generator": ghg_scope3_pie_chart.ghg_scope3_pie_chart_from_db,
#         "params": {},
#     },
# }


class Charts:
    def __init__(self, chart_type, company_id):
        self.chart_type = chart_type
        self.company_id = company_id
        self.fig = None

    def build_save(self):
        self.build()
        return self.save()

    def save(self):
        if self.fig:
            config = {"displaylogo": False, "responsive": True}
            name_fig = self.chart_type["name"] + str(self.company_id)
            filepath_img = os.path.join(
                settings.BASE_DIR,
                "static",
                "django_project",
                "images",
                "charts",
                self.chart_type["name"],
            )

            filepath_plot = os.path.join(
                settings.BASE_DIR,
                "templates",
                "django_project",
                "corporates",
                "charts",
                "html_exports",
                self.chart_type["name"],
            )

            self.fig.write_image(os.path.join(filepath_img, f"{name_fig}.jpeg"))
            plot(
                self.fig,
                config=config,
                filename=os.path.join(filepath_plot, f"{name_fig}.html"),
                auto_open=False,
            )
        else:
            return self.company_id

    def build(self):
        self.fig = self.chart_type["generator"](
            self.company_id, self.chart_type["params"]
        )


def produce_charts(id_list, chart_type):
    """
    Produces a chart for each company_id in id_list
    The type of the chart is defined by chart_type that is an instance of CHART_TYPES
    """

    all_res = []
    for idx in id_list:
        res = Charts(chart_type=chart_type, company_id=idx).build_save()
        if res:
            all_res.append(res)
    return all_res
