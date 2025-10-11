import sqlite3
from plan import Plan
from constants import mile_conversion

def dict_factory(cursor, row): 
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#TODO need to add user to the sql calls to support multiple data in the future
def get_week_data(runner):
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute(f"SELECT * FROM week WHERE runner_id = {runner} ORDER BY week ASC")
    weeks = c.fetchall()
    conn.close()
    for week in weeks:
        week["total_distance"] = round(week["total_distance"] / mile_conversion, 2) if isinstance(week["total_distance"], (float, int)) else 0
        week["easy_distance"] = round(week["easy_distance"] / mile_conversion, 2) if isinstance(week["easy_distance"], (float, int)) else 0
        week["hard_distance"] = round(week["hard_distance"] / mile_conversion, 2) if isinstance(week["hard_distance"], (float, int)) else 0
        week["lt1_distance"] = round(week["lt1_distance"] / mile_conversion, 2) if isinstance(week["lt1_distance"], (float, int)) else 0
        week["lt2_distance"] = round(week["lt2_distance"] / mile_conversion, 2) if isinstance(week["lt2_distance"], (float, int)) else 0
        week["hard_reps_long_distance"] = round(week["hard_reps_long_distance"] / mile_conversion, 2) if isinstance(week["hard_reps_long_distance"], (float, int)) else 0
        week["hard_reps_short_distance"] = round(week["hard_reps_short_distance"] / mile_conversion, 2) if isinstance(week["hard_reps_short_distance"], (float, int)) else 0
    return weeks

def get_week_data_all():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute(f"SELECT * FROM week ORDER BY week ASC")
    weeks = c.fetchall()
    conn.close()
    for week in weeks:
        week["total_distance"] /= mile_conversion if type(week["total_distance"]) == float else 0
        week["easy_distance"] /= mile_conversion if type(week["easy_distance"]) == float else 0
        week["hard_distance"] /= mile_conversion if type(week["hard_distance"]) == float else 0
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
            total_distance = days[day]["total_distance"] / mile_conversion if type(days[day]["total_distance"]) == float else 0
            hard_pace = days[day]["hard_pace"]

            days_dict["week"].append(week)
            days_dict["day"].append(day)
            days_dict["total_distance"].append(total_distance)
            days_dict["hard_pace"].append(hard_pace)

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

def get_plan_data(runner):
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory  
    c = conn.cursor()
    c.execute(f"SELECT * FROM plan WHERE runner = {runner} ORDER BY week ASC")
    plans = c.fetchall()
    conn.close()
    return plans

def get_running_gear(runner):
    conn = sqlite3.connect('runner.db')
    conn.row_factory = dict_factory  
    c = conn.cursor()
    c.execute(f"SELECT * FROM gear WHERE runner = {runner}")
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