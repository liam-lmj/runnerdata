import sqlite3

#TODO need to add user to the sql calls to support multiple data in the future

def get_week_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute("SELECT * FROM week ORDER BY week ASC")
    weeks = c.fetchall()
    conn.close()
    return weeks

def get_days_day(weeks):
    days_dict = {
    "week": [],
    "day": [],
    "total_distance": [],
    "hard_pace": []
    }

    for row in weeks:
        week = row["week"]
        days = eval(row["days"])

        for day in days:
            days_dict["week"].append(week)
            days_dict["day"].append(day)
            days_dict["total_distance"].append(days[day]["total_distance"])
            days_dict["hard_pace"].append(days[day]["hard_pace"])

    return days_dict

week_data = get_week_data()
get_days_day(week_data)