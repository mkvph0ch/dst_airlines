import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import globals
import requests
from mongodb import get_geopositions_from_airlabs
import time
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
globals.initialize()

#_, df = get_geopositions_from_airlabs(globals.airlabs_token)

app.layout = html.Div(children=[
    html.H1(children='DST Airlines'),
    html.Div(children='''
        This data was provided by the Airlabs API https://airlabs.co.
    '''),

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
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    _, df = get_geopositions_from_airlabs(globals.airlabs_token)

    # Create the graph with subplots
    fig = go.Figure(data=go.Scattergeo(
        lon=df['lng'],
        lat=df['lat'],
        text=df['flight_number'],
        mode='markers'
    ))

    fig.update_layout(
        geo_scope='world',
        title_text=f"Interval {n}"
    )

    return fig

if __name__ == '__main__':    
    app.run_server(debug=True)
    