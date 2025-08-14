import sqlite3
import pandas as pd 
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
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

df_week = pd.DataFrame(map(dict, get_week_data()))
df_days = pd.DataFrame(get_days_day(get_week_data()))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
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
                html.H4("Daily Mileage", className="card-title"),
                dcc.Dropdown(sorted(df_days["week"].unique(), reverse=True), sorted(df_days["week"].unique(), reverse=True)[0], id="daily_pace_graph_item"),
                dcc.Graph(id="daily_pace_graph")
            ])
        ], width=6)
    ])

])

@callback(
    Output(component_id='distance_graph', component_property='figure'),
    Input(component_id='distance_graph_item', component_property='value')
)
def mileage_graph(col_chosen):
    fig = px.bar(df_week, x="week", y=col_chosen,  title="Weekly Mileage")
    return fig

@callback(
    Output(component_id='pace_graph', component_property='figure'),
    Input(component_id='pace_graph_item', component_property='value')
)
def pace_graph(col_chosen):
    fig = px.line(df_week, x="week", y=col_chosen,  title="Pace Trend")
    return fig

@callback(
    Output(component_id='days_graph', component_property='figure'),
    Input(component_id='days_graph_item', component_property='value')
)
def days_graph(col_week):
    filtered_df = df_days[df_days['week'] == col_week]
    fig = px.pie(filtered_df, values="total_distance", names="day",  title="Pace Trend")
    return fig

@callback(
    Output(component_id='daily_pace_graph', component_property='figure'),
    Input(component_id='daily_pace_graph_item', component_property='value')
)
def daily_pace_graph(col_week):
    filtered_df = df_days[(df_days['week'] == col_week) & (df_days['hard_pace'] > 0)]
    fig = px.line(filtered_df, x="day", y="hard_pace",  title="Daily Session Pace Trend")
    return fig

if __name__ == '__main__':
    app.run(debug=True)