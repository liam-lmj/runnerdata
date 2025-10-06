import json
import plotly
import plotly.express as px
from datetime import datetime, timedelta
from constants import days_in_week, week_order, days_of_week, mile_conversion

def current_week_year():
    now = datetime.now()
    week_year = now.strftime("%W-%Y")
    return week_year

def previous_week_year():
    now = datetime.now()
    last_week = now - timedelta(days=7)
    week_year = last_week.strftime("%W-%Y")
    return week_year

def get_next_five_weeks():
    next_five_weeks = []

    date = datetime.now()
    for i in range(1,6):
        date += timedelta(days=7)
        week_year = date.strftime("%W-%Y")
        next_five_weeks.append(week_year)

    return next_five_weeks

def get_weekly_mileage(week_data):
    weekly_mileage = []

    for week in week_data:
        days = week["days"]
        days_dict = eval(days)
        sorted_dict = {}
        total_distance = 0
        easy_distance = 0
        hard_distance = 0
        hard_time = 0 
        hard_pace = 0
        for day in week_order:
            if day in days_dict:
                sorted_dict[days_of_week[day]] = days_dict[day]
                total_distance += days_dict[day]["total_distance"]
                easy_distance += days_dict[day]["easy_distance"]
                hard_distance += days_dict[day]["hard_distance"]
                hard_time += days_dict[day]["hard_distance"] * days_dict[day]["hard_pace"]

        if hard_distance > 0:
            hard_pace = round((hard_time / hard_distance), 2)
        
        sorted_dict["Total"] = {"total_distance": total_distance, 
                                "easy_distance": easy_distance,
                                "hard_distance": hard_distance,
                                "hard_pace": hard_pace}

        if len(days_dict) == days_in_week:
            sorted_dict["week"] = week["week"]
            weekly_mileage.append(sorted_dict)

    weekly_mileage.reverse()    

    return weekly_mileage

def pie_chart(week, df_week):
    filtered_df_weeks = (df_week[df_week['week'] == week])
    easy_distance = float(filtered_df_weeks['easy_distance'].sum()) / mile_conversion
    hard_distance = float(filtered_df_weeks['hard_distance'].sum()) / mile_conversion
    total = round(easy_distance + hard_distance, 2)
    pie_df = ({
        'Types': ['Easy Miles', 'Hard Miles'],
        'Distance': [easy_distance, hard_distance]
    })
    fig_pie = px.pie(pie_df, names="Types", values="Distance", hole=.6)

    fig_pie.add_annotation(
    text=f"{total} Miles",
    x=0.5,
    y=0.5,
    showarrow=False,
    font_size=18,
    )

    pie_json = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_json


def bar_chart(week, df_days):
    filtered_df_days = (df_days[df_days['week'] == week]
                .assign(Miles=lambda x: round(x['total_distance'] / mile_conversion, 2))
                .assign(Days=lambda x: x['day'].map(days_of_week))
                .assign(order=lambda x: x['day'].map({day: i for i, day in enumerate(week_order)}))
                .sort_values('order')
                )
    fig_bar = px.bar(filtered_df_days, x="Days", y="Miles", color="Days")
    fig_bar.update_traces(showlegend=False)
    bar_json = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_json

def bar_chart_plan(week, df_plans):
    filtered_df_days = (df_plans[df_plans['week'] == week])
    filtered_df_days.columns = [col.capitalize() for col in filtered_df_days.columns]
    days = list(days_of_week.values())
    y_values = filtered_df_days[days].iloc[0]

    fig_bar = px.bar(x=days, y=y_values, color=days)
    fig_bar.update_traces(showlegend=False)
    fig_bar.update_layout(
                            xaxis_title='Days',
                            yaxis_title='Miles'
                        )
    bar_json = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    return bar_json