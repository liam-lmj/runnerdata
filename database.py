import sqlite3

def dict_factory(cursor, row): 
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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

def get_plan_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory  
    c = conn.cursor()
    c.execute("SELECT * FROM plan ORDER BY week ASC")
    plans = c.fetchall()
    conn.close()
    for plan in plans:
        for key, value in plan.items():
            if key != "week":
                plan[key] = eval(value)
    return plans

def get_running_gear():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory  
    c = conn.cursor()
    c.execute("SELECT * FROM gear")
    gear = c.fetchall()
    conn.close()
    return gear

def get_gear_by_id(gear_id):
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"SELECT * FROM gear WHERE gear_id = {gear_id}")
    gear = c.fetchone()
    conn.close()
    return gear
