import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

df = pd.read_csv("formatted_output.csv")
df["date"] = pd.to_datetime(df["date"]) 
df = df.sort_values(by="date") 


app = dash.Dash(__name__)


fig = px.line(
    df, 
    x="date", 
    y="sales", 
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"} 
)


app.layout = html.Div(children=[
    html.H1(children="Soul Foods Sales Visualizer"), 
    
    dcc.Graph(
        id="sales-line-chart",
        figure=fig 
    )
])

if __name__ == "__main__":
    app.run(debug=True)