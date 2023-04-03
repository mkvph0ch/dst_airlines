import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import globals
import requests
from mongodb import get_geopositions_from_airlabs

app = dash.Dash(__name__)
globals.initialize()

def get_geopositions():
    
    globals.initialize()
    my_params = {'api_key': globals.airlabs_token}

    method = 'flights'
    api_base = 'http://airlabs.co/api/v9/'

    r = requests.get(api_base + method, params = my_params).json()

    resp_list = r.get("response")

    df = pd.json_normalize(resp_list)

    return df

_, df = get_geopositions_from_airlabs(globals.airlabs_token)

fig = go.Figure(data=go.Scattergeo(
    lon=df['lng'],
    lat=df['lat'],
    text=df['flight_number'],
    mode='markers'
))

fig.update_layout(
    geo_scope='world'
)

app.layout = html.Div(children=[
    html.H1(children='DST Airlines'),
    html.Div(children='''
        This data was provided by the Airlabs API https://airlabs.co.
    '''),

    dcc.Graph(
        id='example-map',
        figure=fig
    )
])

if __name__ == '__main__':    
    app.run_server(debug=True)
    