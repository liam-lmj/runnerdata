import pandas as pd
from flask import Blueprint, render_template, redirect, session, request, jsonify
from appdata import get_weekly_mileage, previous_week_year, bar_chart, pie_chart
from database import get_week_data, get_days_day, get_runner_zones
from appsettings import update_settings

mileage_log_bp = Blueprint('mileage', __name__)

@mileage_log_bp.route("/mileagelog", methods=['GET', 'POST'])
def mileage():
    if not 'user_id' in session:
        return redirect("/")
    runner = session['user_id']
    unit, method, lt1, lt2, hard = get_runner_zones(runner)

    if request.method == "POST":       
        if request.json["type"] == "Settings":
            return update_settings(request.json)
    
    week_data = get_week_data(session['user_id'])
    weekly_mileage = get_weekly_mileage(week_data)

    return render_template("mileagelog.html", 
                           weekly_mileage=weekly_mileage, 
                           unit=unit, 
                           method=method, 
                           lt1=lt1, 
                           lt2=lt2, 
                           hard=hard)

@mileage_log_bp.route("/mileagechart", methods=['GET', 'POST'])
def mileagev2():
    if not 'user_id' in session:
        return redirect("/")
    runner = session['user_id']
    unit, method, lt1, lt2, hard = get_runner_zones(runner)
    week_data = get_week_data(runner)
    weekly_mileage = get_weekly_mileage(week_data)

    df_week = pd.DataFrame(map(dict, week_data))
    df_days = pd.DataFrame(get_days_day(week_data))
    bar_json = bar_chart(previous_week_year(), df_days)
    pie_json = pie_chart(previous_week_year(), df_week)
    week = previous_week_year()
    if request.method == "POST":
        
        if request.json["type"] == "Settings":
            return update_settings(request.json)
        
        week = request.json["selectedWeek"]
        bar_json = bar_chart(week, df_days)
        pie_json = pie_chart(week, df_week)
        return jsonify({"success": True, "bar_json": bar_json, "pie_json": pie_json})
    

    return render_template("mileagechart.html", 
                           bar_json=bar_json, 
                           pie_json=pie_json, 
                           weekly_mileage=weekly_mileage, 
                           week=week, 
                           unit=unit, 
                           method=method, 
                           lt1=lt1, 
                           lt2=lt2, 
                           hard=hard)