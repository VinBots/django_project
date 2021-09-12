from chart_types import bubble_charts, bullet_charts, ghg_bar_charts, ghg_scope3_pie_chart
from plotly.offline import plot


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
            config = {
                'displaylogo': False,
                'responsive': True
                }
            name_fig = self.chart_type["name"] + str(self.company_id)
            
            self.fig.write_image(
                "../django_project/static/django_project/images/charts/{}/{}.jpeg".format(
                    self.chart_type["name"],
                    name_fig),
                scale=3,
                )
            
            plot(
                self.fig,
                config=config,
                filename = '../django_project/templates/django_project/corporates/charts/html_exports/{}/{}.html'.format(
                    self.chart_type["name"],
                    name_fig),
                auto_open=False)
            """
            chart_div = plot(
                self.fig,
                config=config,
                image_width='100%',
                image_height='100%',
                output_type='div')
            print (chart_div)
            """
        else:
            return self.company_id
    
    def build (self):
        self.fig = self.chart_type["generator"](
            self.company_id,
            self.chart_type["params"]
            )


def produce_charts(id_list, chart_type):
    """
    Produces a chart for each company_id in id_list
    The type of the chart is defined by chart_type that ia an instance of CHART_TYPES
    """

    all_res = []
    for idx in id_list:
        
        res = Charts(
            chart_type = chart_type,
            company_id = idx).build_save()
        if res:
            all_res.append(res)
    
    return all_res


if __name__ == "__main__":

    id_list = list(range(1, 5, 1))

    CHART_TYPES = {
        "bullet":{
            "name":"bullet",
            "generator": bullet_charts.bullet_chart_from_xls,
            "params": {
                "year": "2019",
            },
        },
        "bubble":{
            "name":"bubble",
            "generator": bubble_charts.bubble_chart_from_xls,
            "params": {
                "year": "2019",
            },
        },
        "ghg_bar":{
            "name":"ghg_bar",
            "generator": ghg_bar_charts.ghg_bar_chart_from_xls,
            "params": {},
        },
        "ghg_pie_chart":{
            "name":"ghg_pie_chart",
            "generator": ghg_scope3_pie_chart.ghg_scope3_pie_chart_from_xls,
            "params": {},
        }
    }

    res = produce_charts(id_list, CHART_TYPES["bubble"])
    print ("Number of failures = {} for company ids = {}".format(len(res), res))