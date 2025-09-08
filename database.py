import sqlite3
from plan import Plan

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

def update_pending_plans(runner):
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory  
    c = conn.cursor()
    c.execute(f"SELECT * FROM plan WHERE achieved != 'pending' and runner = {runner}")
    plans = c.fetchall()
    conn.close()
    for record in plans:
        plan = Plan(record)
        plan.update_current()
        plan.update_vs_week()
        if plan.plan_exists():
            plan.update_plan()
        else:
            plan.insert_plan()

def get_plan_data():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory  
    c = conn.cursor()
    c.execute("SELECT * FROM plan ORDER BY week ASC")
    plans = c.fetchall()
    conn.close()
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

def get_easy_and_hard_gear():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"SELECT gear_id, distance, default_type FROM gear WHERE default_type in ('Easy', 'Hard')")
    gear = c.fetchall()
    conn.close()
    return gear

def update_gear(easy_distance, hard_distance):
    gear_to_update = get_easy_and_hard_gear()
    conn = sqlite3.connect('runner.db')
    c = conn.cursor()
    for gear in gear_to_update:
        current_distance = gear["distance"]
        new_miles = current_distance + easy_distance if gear["default_type"] == 'Easy' else current_distance + hard_distance   
        c.execute(
            "UPDATE gear SET distance = ? WHERE gear_id = ?",
            (new_miles, gear["gear_id"])
        )        
    conn.commit()
    conn.close()