import pandas as pd 
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_callbacks
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from database import get_week_data, get_days_day

def init_dashboard(server, df_week, df_days):

    dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, url_base_pathname="/dash/")

    dash_app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Running Data"), width=12, className="text-center my-5")
        ]),

        dbc.Row([
            dbc.Col([
                dbc.CardBody([
                    html.H4("Mileage Graph", className="card-title"),
                    dcc.Dropdown(['total_distance', 'easy_distance', 'hard_distance'], 'total_distance', id="distance_graph_item"),
                    dcc.Graph(id="distance_graph")
                ])
            ], width=6),
            dbc.Col([
                dbc.CardBody([
                    html.H4("Pace Graph", className="card-title"),
                    dcc.Dropdown(['easy_pace', 'hard_pace'], 'hard_pace', id="pace_graph_item"),
                    dcc.Graph(id="pace_graph")
                ])
            ], width=6)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.CardBody([
                    html.H4("Daily Mileage", className="card-title"),
                    dcc.Dropdown(sorted(df_days["week"].unique(), reverse=True), sorted(df_days["week"].unique(), reverse=True)[0], id="days_graph_item"),
                    dcc.Graph(id="days_graph")
                ])
            ], width=6), 
            dbc.Col([
                dbc.CardBody([
                    html.H4("Daily Session Pace Trend", className="card-title"),
                    dcc.Dropdown(sorted(df_days["week"].unique(), reverse=True), sorted(df_days["week"].unique(), reverse=True)[0], id="daily_pace_graph_item"),
                    dcc.Graph(id="daily_pace_graph")
                ])
            ], width=6)
        ])
    ])

    dash_callbacks.register_callbacks(dash_app, df_week, df_days)

    return dash_app