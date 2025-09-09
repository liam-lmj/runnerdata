import pandas as pd 
from plan import Plan
from gear import Gear
from appdata import get_next_five_weeks, get_weekly_mileage, current_week_year, bar_chart, pie_chart, previous_week_year, bar_chart_plan
from flask import Flask, render_template, request, jsonify, send_from_directory
from dashboard import init_dashboard
from database import get_week_data, get_days_day, get_plan_data, get_running_gear, get_gear_by_id
from constants import days_of_week, run_types

app = Flask(__name__)

current_week = current_week_year()
week_data = get_week_data()
df_week = pd.DataFrame(map(dict, week_data))
df_days = pd.DataFrame(get_days_day(week_data))

weekly_mileage = get_weekly_mileage(week_data)
next_five_weeks = get_next_five_weeks()

training_plans = get_plan_data()
df_plans = pd.DataFrame(training_plans)

init_dashboard(app, df_week, df_days)

#to deliver banner to dash app
@app.route("/bannerdash.html")
def serve_banner():
    return send_from_directory("templates", "bannerdash.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mileagelog")
def mileage():
    return render_template("mileagelog.html", weekly_mileage=weekly_mileage)

@app.route("/gear", methods=["GET", "POST"])
def gear():
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

@app.route("/trainingform", methods=["GET", "POST"])
def trainingplanform():
    return render_template("trainingplanform.html", days_of_week=days_of_week, next_five_weeks=next_five_weeks)

@app.route("/training", methods=["GET", "POST"])
def trainingplan():
    bar_json_plans = bar_chart_plan(current_week_year(), df_plans)
    if request.method == "POST": 
        plan = Plan(request.json)
        if plan.plan_exists():
            plan.update_plan()
            plan.update_vs_week()
        else:
            plan.insert_plan()

    return render_template("training.html", training_plans=training_plans, bar_json_plans=bar_json_plans,current_week=current_week, next_five_weeks=next_five_weeks)

@app.route("/mileagechart", methods=['GET', 'POST'])
def mileagev2():
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