import dash_bootstrap_components as dbc
import dash_callbacks
from dash import Dash, html, dcc

def init_dashboard(server, df_days):

    dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, url_base_pathname="/dash/")

    def layout():
        return html.Div([
            html.Div(
                html.Iframe(
                    src="/bannerdash.html",
                    style={"width": "100%", "height": "110px", "border": "none"}
                ),
                style={"width": "100%"}
            ),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.CardBody([
                            html.H4("Mileage Graph", className="card-title"),
                            dcc.Dropdown(
                                ['Total Distance', 'Easy Distance', 'Total Hard Distance', 'LT1 Distance', 'LT2 Distance', 'Long Reps Distance', 'Short Reps Distance'],
                                'Total Distance',
                                id="distance_graph_item"
                            ),
                            dcc.Graph(id="distance_graph")
                        ])
                    ], width=6),

                    dbc.Col([
                        dbc.CardBody([
                            html.H4("Pace Graph", className="card-title"),
                            dcc.Dropdown(
                                ['Easy Pace', 'Hard Pace', 'LT1 Pace', 'LT2 Pace', 'Long Reps Pace', 'Short Reps Pace'],
                                'Hard Pace',
                                id="pace_graph_item"
                            ),
                            dcc.Graph(id="pace_graph")
                        ])
                    ], width=6)
                ]),

                dbc.Row([
                    dbc.Col([
                        dbc.CardBody([
                            html.H4("Daily Mileage", className="card-title"),
                            dcc.Dropdown(
                                sorted(df_days["week"].unique(), reverse=True),
                                sorted(df_days["week"].unique(), reverse=True)[0],
                                id="days_graph_item"
                            ),
                            dcc.Graph(id="days_graph")
                        ])
                    ], width=6),

                    dbc.Col([
                        dbc.CardBody([
                            html.H4("Daily Session Pace Trend", className="card-title"),
                            dcc.Dropdown(
                                sorted(df_days["week"].unique(), reverse=True),
                                sorted(df_days["week"].unique(), reverse=True)[0],
                                id="daily_pace_graph_item"
                            ),
                            dcc.Graph(id="daily_pace_graph")
                        ])
                    ], width=6)
                ])
            ])
        ])

    dash_app.layout = layout

    dash_callbacks.register_callbacks(dash_app)

    return dash_app