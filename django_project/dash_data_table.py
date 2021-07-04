import dash
import dash_table
import pandas as pd
from django_plotly_dash import DjangoDash


app = DjangoDash('data_table')
'''
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
'''
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)

app = DjangoDash('data_table')

PAGE_SIZE = 5

app.layout = dash_table.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "id": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom'
)


if __name__ == '__main__':
    app.run_server(debug=True)