import pandas as pd 
from flask import Flask, render_template, request
from dashboard import init_dashboard
from database import get_week_data, get_days_day
from constants import days_in_week, week_order, days_of_week

app = Flask(__name__)

week_data = get_week_data()
df_week = pd.DataFrame(map(dict, week_data))
df_days = pd.DataFrame(get_days_day(week_data))

init_dashboard(app, df_week, df_days)

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mileage")
def mileage():
    return render_template("mileagechart.html", weekly_mileage=weekly_mileage)

if __name__ == "__main__":
    app.run(debug=True)