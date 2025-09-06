import pandas as pd 
from plan import Plan
from gear import Gear
from appdata import get_next_five_weeks, get_weekly_mileage, current_week_year
from flask import Flask, render_template, request, jsonify
from dashboard import init_dashboard
from database import get_week_data, get_days_day, get_plan_data, get_running_gear
from constants import days_of_week, run_types

app = Flask(__name__)

current_week = current_week_year()
week_data = get_week_data()
df_week = pd.DataFrame(map(dict, week_data))
df_days = pd.DataFrame(get_days_day(week_data))

weekly_mileage = get_weekly_mileage(week_data)
next_five_weeks = get_next_five_weeks()

#running_gear = get_running_gear()

init_dashboard(app, df_week, df_days)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mileagelog")
def mileage():
    return render_template("mileagechart.html", weekly_mileage=weekly_mileage)

@app.route("/gear", methods=["GET", "POST"])
def gear():
    running_gear = get_running_gear()
    if request.method == "POST":
        gear_updates = request.json
        print(gear_updates)
        if gear_updates["type"] == "Update":
            total_new_miles = gear_updates["totalNewMiles"]
            gear_id = gear_updates["gear_id"]
            gear_data = running_gear[int(gear_id) - 1] #gear_id starts at 1 in database and list is 0 indexed

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
            print(gear)

            gear.insert_gear()

        return jsonify({"success": True})
    

    return render_template("gear.html", running_gear=running_gear)

@app.route("/trainingform", methods=["GET", "POST"])
def trainingplanform():
    return render_template("trainingplanform.html", days_of_week=days_of_week, next_five_weeks=next_five_weeks)

@app.route("/training", methods=["GET", "POST"])
def trainingplan():
    if request.method == "POST": 
        plan = Plan(request.form.to_dict())
        if plan.plan_exists():
            plan.update_plan()
        else:
            plan.insert_plan()      
    training_plans = get_plan_data()
    return render_template("training.html", training_plans=training_plans, current_week=current_week)

if __name__ == "__main__":
    app.run(debug=True)