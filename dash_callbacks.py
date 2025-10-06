import plotly.express as px
import pandas as pd 
from database import get_week_data, get_days_day
from dash import Input, Output
from flask import session
from constants import days_of_week, week_order

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
        filtered_df.rename(columns={'easy_distance': 'Easy Distance', 
                                    'hard_distance': 'Hard Distance', 
                                    'total_distance': 'Total Distance', 
                                    'week': 'Week'}, 
                                    inplace=True)

        fig = px.bar(filtered_df, x="Week", y=col_chosen, title="Weekly Mileage")
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
        filtered_df.rename(columns={'easy_pace': 'Easy Pace', 
                                    'hard_pace': 'Hard Pace', 
                                    'week': 'Week'}, 
                                    inplace=True)

        fig = px.line(filtered_df, x="Week", y=col_chosen, title="Pace Trend")
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
        df_days['Day'] = df_days['day'].map(days_of_week)
        filtered_df = df_days[(df_days['week'] == col_week)]
        filtered_df.rename(columns={'total_distance': 'Total Distance'}, inplace=True)

        fig = px.pie(filtered_df, values="Total Distance", names="Day", title="Days Distribution")
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
        df_days['Day'] = df_days['day'].map(days_of_week)
        filtered_df = df_days[(df_days['week'] == col_week) & (df_days['hard_pace'] > 0)]
        filtered_df.rename(columns={'hard_pace': 'Hard Pace'}, inplace=True)

        fig = px.line(filtered_df, x="Day", y="Hard Pace", title="Daily Session Pace Trend")
        return fig
