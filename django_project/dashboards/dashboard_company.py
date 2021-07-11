
from django_plotly_dash import DjangoDash

app = DjangoDash('company_performance_dashboard')
app.layout = html.Div([
        html.Div([
            html.Div([
                html.Div(
                    ["gg",
                    "hh"]),
                html.Div(["company_name"]),])])])