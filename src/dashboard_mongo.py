import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
# import pandas as pd
import globals
# import requests
from mongodb import get_geopositions_from_airlabs, write_mongo, read_mongo
# import time
import datetime
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import psycopg2


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

globals.initialize()

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

    dcc.Dropdown(['All flights', 'Commericial passenger flights only'],
                 'All flights',
                 id='flight-type-dropdown'
    ),

    dcc.Graph(
        id='world-map',
        style={'height': '100%'}
    ),

    html.Div(
        id='flight-info',
        style={'position': 'absolute', 'top': 0, 'right': 0, 'padding': '10px'}
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
    write_mongo(df=df, db='air_traffic_system', collection='positions', host=globals.mongohost)

    df = read_mongo(db='air_traffic_system', collection='positions', host=globals.mongohost)

    last_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Drop rows where either airline_iata or flight_number is missing
    df = df.dropna(subset=['airline_iata', 'flight_number'])

    # checking if the values of flight number match the pattern
    pattern = r'^[a-zA-Z0-9]{2}\d{3,4}$'
    mask = ((df['airline_iata'] + df['flight_number']).str.contains(pattern, na=False)) | (df['flight_iata'].str.contains(pattern, na=False))
    df = df.loc[mask, :].copy()
    df['flight_number_final'] = df['airline_iata'] + df['flight_number']
    df.loc[~df['flight_number_final'].str.contains(pattern, na=False), 'flight_number_final'] = df['flight_iata']


    # Create the graph with subplots
    fig = go.Figure(data=go.Scattergeo(
        lon=df['lng'],
        lat=df['lat'],
        # text=df['airline_iata'] + df['flight_number'],
        text=df['flight_number_final'],
        mode='markers',
        marker=dict(
            color='blue'
        ),
        geojson='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
                '/world-countries.json',
        featureidkey='properties.name',
        texttemplate='%{properties.name}', # use the country name from the GeoJSON file as text
        showlegend=True,
     ))

    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="LightGreen",
            showocean=True,
            oceancolor="LightBlue",
            showcountries=True,
            countrycolor="Black",
            showsubunits=True, 
            subunitcolor="Blue"
        ),
        title_text=f"Interval {n}. Last Update {last_timestamp}"
    )

    return fig


# div with flight information
@app.callback(Output('flight-info', 'children'),
              [Input('world-map', 'clickData')])
def display_flight_info(clickData):
    if clickData is not None:
        flight_number = clickData['points'][0]['text']
        ####### for test  #######
        # flight_number = 'LH1961' 

        df_flights = read_mongo(db='air_traffic_system', collection='flights', host=globals.mongohost)

        df_flights = df_flights.dropna(subset=['OperatingCarrier.AirlineID', 'OperatingCarrier.FlightNumber'])
        df_flights['flight_number_final'] = df_flights['OperatingCarrier.AirlineID'] + df_flights['OperatingCarrier.FlightNumber'].astype(str)
        df_flights = df_flights[df_flights['flight_number_final'] == flight_number]  # filter by flight_number
        
        # df_flights = df_flights[df_flights['Arrival.Scheduled.Date'] > datetime.now()]  # filter by future date
        # TODO: add filter by date or by flight status
        # TODO: display dates and times
        
        if len(df_flights) == 0:
            return html.Div([
                html.P("No data found for the selected flight number"),
                html.P(flight_number)
            ])
        
        dep_airport = df_flights['Departure.AirportCode'].iloc[0]  # select the first airport code
        arr_airport = df_flights['Arrival.AirportCode'].iloc[0]  # select the first airport code

        dep_country, dep_city = get_city_country_by_airport(dep_airport)
        arr_country, arr_city = get_city_country_by_airport(arr_airport)

        return html.Div(children=[
            html.H1(children=flight_number),
            html.Div(children=f"{dep_city}, {dep_country} ({dep_airport}) --> {arr_city}, {arr_country} ({arr_airport})")
        ]) 
    else:
        return html.Div([
            html.P("Click on a flight to display its information")
        ])


def get_city_country_by_airport(airport_code):
    
    # create a connection to the PostgreSQL database
    conn = psycopg2.connect(host=globals.hostname,
                        dbname=globals.database,
                        user=globals.username,
                        password=globals.pwd,
                        port=globals.port_id)

    cur = conn.cursor()
    sql_query = f"SELECT CountryName, CityName FROM mv_airports_detailed WHERE AirportCode = upper('{airport_code}');"
    cur.execute(sql_query)
    results = cur.fetchall()
    if len(results) > 0:
      country = results[0][0]
      city = results[0][1]
    else:
      return '',''

    cur.close()
    conn.close()

    return country, city

    
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)