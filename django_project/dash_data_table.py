import dash
import dash_table
import pandas as pd
from django_plotly_dash import DjangoDash

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = DjangoDash('data_table')

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)