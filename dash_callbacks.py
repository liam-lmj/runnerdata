import plotly.express as px
import pandas as pd 
from database import get_week_data, get_days_day
from dash import Input, Output
from flask import session

def register_callbacks(dash_app):
    @dash_app.callback(
        Output("distance_graph", "figure"),
        Input("distance_graph_item", "value")
    )
    def mileage_graph(col_chosen):        
        if 'user_id' not in session:
            return {}
        runner = session['user_id']
        week_data = get_week_data(runner)
        filtered_df = pd.DataFrame(map(dict, week_data))

        fig = px.bar(filtered_df, x="week", y=col_chosen, title="Weekly Mileage")
        return fig

    @dash_app.callback(
        Output("pace_graph", "figure"),
        Input("pace_graph_item", "value")
    )
    def pace_graph(col_chosen):
        if 'user_id' not in session:
            return {}
        runner = session['user_id']
        week_data = get_week_data(runner)
        filtered_df = pd.DataFrame(map(dict, week_data))

        fig = px.line(filtered_df, x="week", y=col_chosen, title="Pace Trend")
        return fig

    @dash_app.callback(
        Output("days_graph", "figure"),
        Input("days_graph_item", "value")
    )
    def days_graph(col_week):
        if 'user_id' not in session:
            return {}
        runner = session['user_id']
        week_data = get_week_data(runner)
        df_days = pd.DataFrame(get_days_day(week_data))
        filtered_df = df_days[(df_days['week'] == col_week)]

        fig = px.pie(filtered_df, values="total_distance", names="day", title="Days Distribution")
        return fig

    @dash_app.callback(
        Output("daily_pace_graph", "figure"),
        Input("daily_pace_graph_item", "value")
    )
    def daily_pace_graph(col_week):
        if 'user_id' not in session:
            return {}
        runner = session['user_id']
        week_data = get_week_data(runner)
        df_days = pd.DataFrame(get_days_day(week_data))
        filtered_df = df_days[(df_days['week'] == col_week) & (df_days['hard_pace'] > 0)]

        fig = px.line(filtered_df, x="day", y="hard_pace", title="Daily Session Pace Trend")
        return fig
