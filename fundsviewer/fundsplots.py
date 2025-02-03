from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


#import asyncio

#from fundsviewer.serviceutils import event_initialized, wait_for_event
#asyncio.run( wait_for_event(event_initialized) )
#from fundsviewer.serviceutils import mainapp

import fundsviewer.fundsviewer


app1 = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    requests_pathname_prefix='/dashboard/'
)

app1.layout = [
    html.H1(children='Example App with Dash', style={'textAlign':'center'}),
    html.Hr(),
    dcc.Dropdown(
        list(fundsviewer.fundsviewer.dataframes.keys()),
        'generali',
        id='dropdown-selection'
    ),
    dcc.Graph(id='graph-content')
]


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = fundsviewer.fundsviewer.dataframes[value]
    return px.line(dff, x=dff.index, y=dff.columns)
