#!/usr/bin/env python
import dash
from dash import dcc
from dash import html
from dash import Input, Output

import plotly.graph_objs as go
import pandas as pd

from assets.colorscales import RdPu, Spectral, Rainbow

dataFrame = pd.read_csv("../source/clustered.csv")

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(id="body", children = [
    html.Div(
        id = "control-tab",
        children = [
            html.H1("Control panel", className = "header"),

            html.Div(className = "nav-item", children = [
                # Gender Selection
                html.Label("Select the Gender", className = "label"),
                dcc.Dropdown(
                    id = "gender-select",
                    options=[
                        {'label': 'Female', 'value': 1},
                        {'label': 'Male', 'value': 0},
                    ],
                    multi = True,
                    value = [0, 1]
                ),]
            ),

            html.Div(className = "nav-item", children = [
                # Age slider selection
                html.Label("Select the Age", className = "label"),
                dcc.RangeSlider(
                    id = "age",
                    min = dataFrame.Age.min(),
                    max = dataFrame.Age.max(),
                    step = 1,
                    allowCross = False,
                    value = [dataFrame.Age.min(), dataFrame.Age.max()],
                    tooltip={"placement": "bottom", "always_visible": True}
                ),]
            ),

            html.Div(className = "nav-item", children = [
                # Annual Income  slider selection
                html.Label("Annual Income", className = "label"),
                dcc.RangeSlider(
                    id = "income",
                    min = dataFrame["Annual Income (k$)"].min(),
                    max = dataFrame["Annual Income (k$)"].max(),
                    step = 1,
                    allowCross = False,
                    value = [dataFrame["Annual Income (k$)"].min(), dataFrame["Annual Income (k$)"].max()],
                    tooltip={"placement": "bottom", "always_visible": True}
                ),]
            ),

            html.Div(className = "nav-item", children = [
                # Annual Income  slider selection
                html.Label("Spending Score (1-100)", className = "label"),
                dcc.RangeSlider(
                    id = "score",
                    min = dataFrame["Spending Score (1-100)"].min(),
                    max = dataFrame["Spending Score (1-100)"].max(),
                    step = 1,
                    allowCross = False,
                    value = [dataFrame["Spending Score (1-100)"].min(), dataFrame["Spending Score (1-100)"].max()],
                    tooltip={"placement": "bottom", "always_visible": True}
                ),]
            ),

        ]
    ),
    html.Div(
        id = "distribution-area", className = "flex-row",
        children = [
            html.Div(id = "gender", children = [dcc.Graph(id = "gender-plot")]),
            html.Div(id = "age-dist", children = [dcc.Graph(id = "age-distribution")]),
        ]
    ),

    html.Div(id = "scatter", children = [dcc.Graph(id = "scatter-map")])

    ]




)

@app.callback(
    Output("gender-plot", "figure"),
    Input("gender-select", "value")
)
def gender_plot(labels:list) -> dict:
    filtered = dataFrame
    values = []
    

    values = [filtered.Genre[(filtered.Genre == 1)].count(), filtered.Genre[(filtered.Genre == 0)].count()]
    label = ["Female", "Male"]

    data = [
        go.Pie(labels = label, values = values, marker = {"colors": [RdPu[0], RdPu[-1]]})
    ]

    layout = go.Layout(
        title = "Male and Female participants in the survey",
        font = {"size": 18, "color": "#fff"},
        paper_bgcolor = 'rgb(0, 0, 0, .65)',
    )

    return dict(data = data, layout = layout)



@app.callback(
    Output("age-distribution", "figure"),
    Input("gender-select", "value"),
    Input("age", "value"),
    Input("income", "value"),
    Input("score", "value"),
)
def gender_dist(labels:list, age:int, income:int, score:int) -> dict:
    filtered = dataFrame
    
    # Gender filtering
    if len(labels) == 1:
        filtered = filtered[filtered["Genre"] == labels[0]]
    
    # Age filtering
    filtered = filtered[
        (filtered["Age"] >= age[0]) & (filtered["Age"] <= age[1])
    ]

    # Income Filtering
    filtered = filtered[
        (filtered["Annual Income (k$)"] >= income[0]) & (filtered["Annual Income (k$)"] <= income[1])
    ]

    # Spending Score Filtering
    filtered = filtered[
        (filtered["Spending Score (1-100)"] >= score[0]) & (filtered["Spending Score (1-100)"] <= score[1])
    ]

    data = [
        go.Histogram(x = filtered["Age"], nbinsx = 12, marker = {"color": RdPu[int(len(RdPu)/2)]})
    ]

    layout = go.Layout(
        title = "Age distribution of participants based on Gender, Annual Income, Spending Score",
        font = {"size": 14, "color": "#fff"},
        xaxis = {"title": "Age distribution", "color": "#fff"},
        yaxis = {"title": "Number of customers", "color": "#fff"},
        showlegend = False,
        paper_bgcolor = 'rgb(0, 0, 0, .65)',
        plot_bgcolor = 'rgb(0, 0, 0, .65)',
        bargap = .04
    )

    return dict(data = data, layout = layout)


@app.callback(
    Output("scatter-map", "figure"),
    Input("gender-select", "value")
)
def scatter(labels:list) -> dict:
    data = [
        go.Scatter(x = dataFrame["Annual Income (k$)"], y = dataFrame["Spending Score (1-100)"], mode = "markers", marker = {"color": dataFrame["Clusters"], "colorscale": Rainbow, "size": 12})
    ]

    layout = go.Layout(
        title = "Predicted clusters based on Annual Income and Spending Score of the Customers",
        font = {"size": 18, "color": "#fff"},
        xaxis = {"title": "Annual Income (k$)", "color": "#fff"},
        yaxis = {"title": "Spending Score (1-100)", "color": "#fff"},
        paper_bgcolor = 'rgb(0, 0, 0, .65)',
        plot_bgcolor = 'rgb(0, 0, 0, .65)',
        height = 700,
    )

    return dict(data = data, layout = layout)












if __name__ == "__main__":
    app.run_server(debug = False)