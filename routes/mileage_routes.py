import pandas as pd
from flask import Blueprint, render_template, redirect, session, request, jsonify
from appdata import get_weekly_mileage, previous_week_year, bar_chart, pie_chart
from database import get_week_data, get_days_day

mileage_log_bp = Blueprint('mileage', __name__)

@mileage_log_bp.route("/mileagelog")
def mileage():
    if not 'user_id' in session:
        return redirect("/")
    week_data = get_week_data(session['user_id'])
    weekly_mileage = get_weekly_mileage(week_data)

    return render_template("mileagelog.html", weekly_mileage=weekly_mileage)

@mileage_log_bp.route("/mileagechart", methods=['GET', 'POST'])
def mileagev2():
    if not 'user_id' in session:
        return redirect("/")
    week_data = get_week_data(session['user_id'])
    weekly_mileage = get_weekly_mileage(week_data)

    df_week = pd.DataFrame(map(dict, week_data))
    df_days = pd.DataFrame(get_days_day(week_data))
    bar_json = bar_chart(previous_week_year(), df_days)
    pie_json = pie_chart(previous_week_year(), df_week)
    week = previous_week_year()
    if request.method == "POST":
        week = request.json["selectedWeek"]
        bar_json = bar_chart(week, df_days)
        pie_json = pie_chart(week, df_week)
        return jsonify({"success": True, "bar_json": bar_json, "pie_json": pie_json})
    
    print(weekly_mileage)

    return render_template("mileagechart.html", bar_json=bar_json, pie_json=pie_json, weekly_mileage=weekly_mileage, week=week)