import sqlite3
import pandas as pd 
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input


def get_week_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute("SELECT * FROM week ORDER BY week ASC")
    weeks = c.fetchall()
    conn.close()
    return weeks

def get_runner_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute("SELECT * FROM runner")
    runners = c.fetchall()
    conn.close()
    return runners

def get_activity_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute("SELECT * FROM activity ORDER BY date ASC")
    activities = c.fetchall()
    conn.close()
    return activities

df_week = pd.DataFrame(map(dict, get_week_data()))
df_runner = pd.DataFrame(map(dict, get_runner_data()))
df_activity = pd.DataFrame(map(dict, get_activity_data()))
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
                html.H4("Place holder 1", className="card-title"),
                dcc.Graph(figure=px.line(df_week, x="week", y="hard_pace",  title="Session Pace"))
            ])
        ], width=6), 
        dbc.Col([
            dbc.CardBody([
                html.H4("Place holder 2", className="card-title"),
                dcc.Graph(figure=px.line(df_week, x="week", y="hard_pace",  title="Session Pace"))
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

if __name__ == '__main__':
    app.run(debug=True)