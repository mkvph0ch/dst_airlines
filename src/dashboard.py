import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
#import globals
import requests
from mongodb import get_geopositions_from_airlabs, load_positions_from_airlabs
import time
import datetime
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

#globals.initialize()

#_, df = get_geopositions_from_airlabs(globals.airlabs_token)

app.layout = html.Div(
    id='main-container',
    style={'width': '100%', 'height': '100vh'},

    children=[
    html.H1(children='DST Airlines'),
    html.Div(children='''
        This data was provided by the Airlabs API https://airlabs.co.
    '''),
    html.Div(children="This project was created by Moldir, Erntam, Sam, Marko"),

    dcc.Graph(
        id='world-map',
        style={'height': '100%'}
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
    _, df = get_geopositions_from_airlabs()
    last_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the graph with subplots
    fig = go.Figure(data=go.Scattergeo(
        lon=df['lng'],
        lat=df['lat'],
        # text=df['airline_iata'] + df['flight_number'],
        text=df['flight_number'],
        mode='markers',
        # marker=dict(
        #     color='blue'
        # ),
        geojson='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
                '/world-countries.json',
        featureidkey='properties.name',
        texttemplate='%{properties.name}', # use the country name from the GeoJSON file as text
        showlegend=True,
     ))

    fig.update_layout(
        geo=dict(
            landcolor="LightGreen",
            oceancolor="LightBlue",
            showocean=True,
            showland=True,
            showcountries=True,
            countrycolor="Black"
        ),
        title_text=f"Interval {n}. Last Update {last_timestamp}"
    )

    return fig

if __name__ == '__main__':    
    app.run_server(debug=True)
    