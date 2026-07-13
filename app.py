import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("formatted_output.csv")
# Preserve original dataframe for callbacks
original_df = df.copy()
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


app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "margin": "40px", "backgroundColor": "#f9f9f9"},
    children=[
        html.H1(
            children="Soul Foods Sales Visualizer",
            style={"textAlign": "center", "color": "#333", "marginBottom": "30px"}
        ),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            labelStyle={"display": "inline-block", "marginRight": "15px"},
            style={"marginBottom": "20px", "textAlign": "center"}
        ),
        dcc.Graph(
            id="sales-line-chart",
            figure=fig,
            style={"height": "600px", "border": "1px solid #e0e0e0", "borderRadius": "8px"}
        )
    ]
)

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all" or not selected_region:
        filtered = original_df.copy()
    else:
        filtered = original_df[original_df["region"].str.lower() == selected_region]
    filtered["date"] = pd.to_datetime(filtered["date"]).sort_values()
    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Total Sales ($)"}
    )
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f9f9f9",
        font=dict(color="#333")
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)