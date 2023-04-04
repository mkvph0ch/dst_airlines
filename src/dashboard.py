import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import globals
import requests
from mongodb import get_geopositions_from_airlabs, load_positions_from_airlabs
import time
import datetime
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
globals.initialize()

#_, df = get_geopositions_from_airlabs(globals.airlabs_token)

app.layout = html.Div(children=[
    html.H1(children='DST Airlines'),
    html.Div(children='''
        This data was provided by the Airlabs API https://airlabs.co.
    '''),
    html.Div(children="This project was created by Moldir, Erntam, Sam, Marko"),

    dcc.Graph(
        id='world-map'
    ),

    dcc.Interval(
        id='interval-component',
        interval=35*1000, # in milliseconds
        n_intervals=0
    )
])

# Multiple components can update everytime interval gets fired.
@app.callback(Output('world-map', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    _, df = get_geopositions_from_airlabs(globals.airlabs_token)
    last_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the graph with subplots
    fig = go.Figure(data=go.Scattergeo(
        lon=df['lng'],
        lat=df['lat'],
        text=df['flight_number'],
        mode='markers'
    ))

    fig.update_layout(
        geo_scope='world',
        autosize=False,
        width=1400,
        height=800,
        margin=dict(
        l=200,
        r=10,
        b=10,
        t=100,
        pad=4
        ),
        title_text=f"Interval {n}. Last Update {last_timestamp}"
    )

    return fig

if __name__ == '__main__':    
    app.run_server(debug=True)
    