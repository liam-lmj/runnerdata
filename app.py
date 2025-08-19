from flask import Flask, render_template, request
from dashboard import init_dashboard

app = Flask(__name__)

init_dashboard(app)

#test data
#TODO pull data from database
#TODO styling for table etc

WEEKLY_MILEAGE = [
    {"week": "week1", "Monday": 10, "Tuesday": 10, "Wednesday": 10, "Thursday": 10,
     "Friday": 12, "Saturday": 12, "Sunday": 14, "total_mileage": 80},
    {"week": "week2", "Monday": 10, "Tuesday": 10, "Wednesday": 10, "Thursday": 10,
     "Friday": 12, "Saturday": 12, "Sunday": 14, "total_mileage": 80}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mileage")
def mileage():
    return render_template("mileagechart.html", weekly_mileage=WEEKLY_MILEAGE)

if __name__ == "__main__":
    app.run(debug=True)