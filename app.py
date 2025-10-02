import os
import pandas as pd 
from plan import Plan
from gear import Gear
from appdata import get_next_five_weeks, get_weekly_mileage, current_week_year, bar_chart, pie_chart, previous_week_year, bar_chart_plan
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect
from dashboard import init_dashboard
from database import get_week_data, get_days_day, get_plan_data, get_running_gear, get_gear_by_id
from constants import  run_types, auth_url
from stravaapi import load_runner, new_access_token
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")

current_week = current_week_year()
week_data = get_week_data()
df_week = pd.DataFrame(map(dict, week_data))
df_days = pd.DataFrame(get_days_day(week_data))

weekly_mileage = get_weekly_mileage(week_data)
next_five_weeks = get_next_five_weeks()

init_dashboard(app, df_week, df_days)

#to deliver banner to dash app
@app.route("/bannerdash.html")
def serve_banner():
    return send_from_directory("templates", "bannerdash.html")

@app.route("/")
def authorise():
    return render_template("authorise.html", auth_url=auth_url)

@app.route("/loaduser")
def loaduser():
    code = request.args.get('code')
    token, runner = load_runner(code) 
    session['user_id'] = runner
    return redirect("/dash")

@app.route("/mileagelog")
def mileage():
    if not 'user_id' in session:
        return redirect("/")
    return render_template("mileagelog.html", weekly_mileage=weekly_mileage)

@app.route("/gear", methods=["GET", "POST"])
def gear():
    if not 'user_id' in session:
        return redirect("/")

    running_gear = get_running_gear()
    if request.method == "POST":
        gear_updates = request.json
        gear_id = None
        if gear_updates["type"] == "Update":
            total_new_miles = gear_updates["totalNewMiles"]
            gear_id = gear_updates["gear_id"]
            gear_data = get_gear_by_id(gear_id)

            deafultType = gear_updates["default_type"] if gear_updates["default_type"] in run_types else None
            active = gear_updates["active"]
            gear = Gear(gear_data["name"], 
                        gear_data["runner"], 
                        gear_data["distance"] + total_new_miles, 
                        active,
                        deafultType,
                        gear_id=gear_data["gear_id"])
            gear.update_gear()
        else:
            gear = Gear(gear_updates["trainer"],
                        "34892346",
                        float(gear_updates["miles"]),
                        "Active",
                        gear_updates["default_type"])
            gear_id = gear.insert_gear()

        return jsonify({"success": True, "gear_id": gear_id})
    

    return render_template("gear.html", running_gear=running_gear)

@app.route("/training", methods=["GET", "POST"])
def trainingplan():
    if not 'user_id' in session:
        return redirect("/")
    training_plans = get_plan_data()
    df_plans = pd.DataFrame(get_plan_data()) if training_plans else None
    inital_week = df_plans['week'].iloc[0]

    bar_json_plans = bar_chart_plan(inital_week, df_plans) if training_plans else None

    if request.method == "POST": 
        if request.json["type"] == "addPlan":
            plan = Plan(request.json)
            if plan.plan_exists():
                plan.update_plan()
                plan.update_vs_week()
            else:
                plan.insert_plan()
            training_plans = get_plan_data()
            return jsonify({"success": True, "training_plans": training_plans})
        
        elif request.json["type"] == "updateChart":
            week = request.json["selectedWeek"]
            bar_json_plans = bar_chart_plan(week, df_plans)
            return jsonify({"success": True, "bar_json": bar_json_plans})

    return render_template("training.html", training_plans=training_plans, bar_json_plans=bar_json_plans,current_week=inital_week, next_five_weeks=next_five_weeks) 

@app.route("/mileagechart", methods=['GET', 'POST'])
def mileagev2():
    if not 'user_id' in session:
        return redirect("/")
    bar_json = bar_chart(previous_week_year(), df_days)
    pie_json = pie_chart(previous_week_year(), df_week)
    week = previous_week_year()
    if request.method == "POST":
        week = request.json["selectedWeek"]
        bar_json = bar_chart(week, df_days)
        pie_json = pie_chart(week, df_week)
        return jsonify({"success": True, "bar_json": bar_json, "pie_json": pie_json})

    return render_template("mileagechart.html", bar_json=bar_json, pie_json=pie_json, weekly_mileage=weekly_mileage, week=week)

if __name__ == "__main__":
    app.run(debug=True)