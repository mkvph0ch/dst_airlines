#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
        id='world-map',
        clickData={'points': [{'customdata': 'FLT1234'}]} # for initial testing only
    ),

    dcc.Interval(
        id='interval-component',
        interval=35*1000, # in milliseconds
        n_intervals=0
    ),

    html.Div(id='flight-info')
])

@app.callback(Output('world-map', 'figure'),
              Input('interval-component', 'n_intervals'),
              State('world-map', 'clickData'))
def update_graph_live(n, clickData):
    _, df = get_geopositions_from_airlabs(globals.airlabs_token)

    # Create the graph with subplots
    fig = go.Figure()

    # Add Scattergeo trace for flights
    fig.add_trace(go.Scattergeo(
        lon=df['lng'],
        lat=df['lat'],
        text=df['flight_number'],
        mode='markers',
        marker=dict(
            color='blue'
        ),
        customdata=df[['flight_number', 'aircraft_name', 'departure_country', 'departure_city', 'departure_time', 'arrival_country', 'arrival_city', 'arrival_time']]
    ))

    # Add Scattermapbox trace for current aircraft position
    if clickData is not None:
        flight_number = clickData['points'][0]['customdata'][0]
        flight_data = clickData['points'][0]['customdata']
        aircraft_name, departure_country, departure_city, departure_time, arrival_country, arrival_city, arrival_time = flight_data[1:]

        lat, lon = df.loc[df['flight_number'] == flight_number, ['lat', 'lng']].values[0]
        fig.add_trace(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            text=f"{flight_number}<br>Aircraft: {aircraft_name}<br>Departure: {departure_country}, {departure_city}, {departure_time}<br>Arrival: {arrival_country}, {arrival_city}, {arrival_time}",
            mode='markers',
            marker=dict(
                symbol='airport',
                size=20,
                color='red'
            )
        ))

        fig.update_layout(
            mapbox=dict(
                center=dict(
                    lat=lat,
                    lon=lon
                ),
                zoom=4
            )
        )

    fig.update_layout(
        geo_scope='world',
        title_text=f"Interval {n}"
    )

    return fig

if __name__ == '__main__':    
    app.run_server(debug=True)

