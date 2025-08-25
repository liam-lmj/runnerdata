import pandas as pd 
from flask import Flask, render_template, request
from dashboard import init_dashboard
from database import get_week_data, get_days_day

app = Flask(__name__)

week_data = get_week_data()
df_week = pd.DataFrame(map(dict, week_data))
df_days = pd.DataFrame(get_days_day(week_data))

init_dashboard(app, df_week, df_days)

#test data
#TODO pull data from database

WEEKLY_MILEAGE = [
    {
        "week": "week1",
        "Monday": {"easy": 10, "hard": 10, "total": 20, "easy_pace": 8, "hard_pace": 5},
        "Tuesday": {"easy": 10, "hard": 0, "total": 10, "easy_pace": 8, "hard_pace": 0},
        "Wednesday": {"easy": 10, "hard": 0, "total": 10, "easy_pace": 8, "hard_pace": 0},
        "Thursday": {"easy": 10, "hard": 0, "total": 10, "easy_pace": 8, "hard_pace": 0},
        "Friday": {"easy": 12, "hard": 0, "total": 12, "easy_pace": 8, "hard_pace": 0},
        "Saturday": {"easy": 12, "hard": 0, "total": 12, "easy_pace": 8, "hard_pace": 0},
        "Sunday": {"easy": 14, "hard": 0, "total": 14, "easy_pace": 8, "hard_pace": 0},
        "Total": {"easy": 14, "hard": 0, "total": 14, "easy_pace": 8, "hard_pace": 0}
    },
    {
        "week": "week2",
        "Monday": {"easy": 10, "hard": 10, "total": 20, "easy_pace": 8, "hard_pace": 5},
        "Tuesday": {"easy": 10, "hard": 0, "total": 10, "easy_pace": 8, "hard_pace": 0},
        "Wednesday": {"easy": 10, "hard": 0, "total": 10, "easy_pace": 8, "hard_pace": 0},
        "Thursday": {"easy": 10, "hard": 0, "total": 10, "easy_pace": 8, "hard_pace": 0},
        "Friday": {"easy": 12, "hard": 0, "total": 12, "easy_pace": 8, "hard_pace": 0},
        "Saturday": {"easy": 12, "hard": 0, "total": 12, "easy_pace": 8, "hard_pace": 0},
        "Sunday": {"easy": 14, "hard": 0, "total": 14, "easy_pace": 8, "hard_pace": 0},
        "Total": {"easy": 14, "hard": 0, "total": 14, "easy_pace": 8, "hard_pace": 0}
    }
]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mileage")
def mileage():
    return render_template("mileagechart.html", weekly_mileage=WEEKLY_MILEAGE)

if __name__ == "__main__":
    app.run(debug=True)