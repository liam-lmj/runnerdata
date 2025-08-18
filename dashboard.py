import sqlite3
import pandas as pd 
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_callbacks
from dash import Dash, html, dash_table, dcc, callback, Output, Input

#TODO need to add user to the sql calls to support multiple data in the future

def get_week_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute("SELECT * FROM week ORDER BY week ASC")
    weeks = c.fetchall()
    conn.close()
    return weeks

def get_days_day(weeks):
    days_dict = {
    "week": [],
    "day": [],
    "total_distance": [],
    "hard_pace": []
    }

    for row in weeks:
        week = row["week"]
        days = eval(row["days"])

        for day in days:
            days_dict["week"].append(week)
            days_dict["day"].append(day)
            days_dict["total_distance"].append(days[day]["total_distance"])
            days_dict["hard_pace"].append(days[day]["hard_pace"])

    return days_dict

def init_dashboard(server):
    week_data = get_week_data()
    df_week = pd.DataFrame(map(dict, week_data))
    df_days = pd.DataFrame(get_days_day(week_data))

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