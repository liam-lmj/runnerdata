import sqlite3
import json
from datetime import datetime, timedelta
from constants import min_miles_conversion

class Week:
    def __init__(self, week, runner_id):
        self.week = week
        self.runner_id = runner_id
        self.days = {}
        self.set_up_total_attributes()

    def get_activities(self):
        week_start = datetime.strptime(f"{self.week}-1 00:00:00", "%W-%Y-%w %H:%M:%S")
        week_end = week_start + timedelta(days=7)

        conn = sqlite3.connect('runner.db')
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()
                
        c.execute(f"""SELECT * 
                    FROM activity
                    WHERE runner_id = {self.runner_id}
                    AND (date BETWEEN DATE('{week_start}') AND DATE('{week_end}'))""")

        activities = c.fetchall()

        conn.commit()
        conn.close()

        return activities

    def set_up_total_attributes(self):
        activities = self.get_activities()
        days = {}
        self.total_distance = 0
        self.hard_distance = 0
        self.easy_distance = 0
        self.session_count = 0
        self.run_count = 0
        self.hard_pace = 0
        self.hard_time = 0
        self.easy_time = 0
        self.easy_pace = 0

        for activity in activities:
            date_string = activity["date"]
            date_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            date_day = date_datetime.strftime("%w")

            easy_distance = activity["easy_distance"]
            hard_distance = activity["hard_distance"]
            run_type = activity["run_type"]
            hard_time = activity["hard_time"]
            easy_time = activity["easy_time"]
            self.total_distance += (easy_distance + hard_distance)
            self.hard_distance += hard_distance
            self.easy_distance += easy_distance
            self.run_count += 1
            self.hard_time += hard_time
            self.easy_time += easy_time
            if run_type == "Session":
                self.session_count += 1
            
            if date_day in days:
                days[date_day]["hard_distance"] += hard_distance
                days[date_day]["easy_distance"] += easy_distance
                days[date_day]["total_distance"] += (hard_distance + easy_distance)
                days[date_day]["hard_time"] += hard_time
                
                days[date_day]["count_of_runs"] += 1
                if run_type == "Session":
                    days[date_day]["count_of_sessions"] += 1
                    if hard_time > 0 and hard_distance > 0:
                        days[date_day]["hard_pace"] = round(min_miles_conversion / (days[date_day]["hard_distance"] / days[date_day]["hard_time"]), 2)
            else:
                day_details = {}

                day_details["hard_distance"] = hard_distance
                day_details["easy_distance"] = easy_distance
                day_details["total_distance"] = hard_distance + easy_distance
                day_details["hard_time"] = hard_time
                day_details["count_of_runs"] = 1
                day_details["count_of_sessions"] = 0
                if run_type == "Session":
                    day_details["count_of_sessions"] += 1
                if hard_time > 0 and hard_distance > 0:
                    day_details["hard_pace"] = round(min_miles_conversion / (hard_distance / hard_time), 2)
                else:
                    day_details["hard_pace"] = 0
                days[date_day] = day_details
        
        if self.hard_distance > 0 and self.hard_time > 0:
            self.hard_pace = round(min_miles_conversion / (self.hard_distance / self.hard_time), 2)
        if self.easy_distance and self.easy_time > 0:
            self.easy_pace = round(min_miles_conversion / (self.easy_distance / self.easy_time), 2)
        self.days = days 

    def week_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM week WHERE week = '{self.week}'")
        exists = c.fetchone()
        conn.close()
        if exists:
            return True
        else:
            return False

    def insert_week(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""INSERT INTO week VALUES 
                  ('{self.week}', 
                  {self.runner_id}, 
                  {self.total_distance},
                  {self.hard_distance},
                  {self.easy_distance},
                  {self.session_count},
                  {self.hard_pace},
                  {self.run_count},
                  '{json.dumps(self.days)}',
                  {self.hard_time},
                  {self.easy_pace,},
                  {self.easy_time})
                  """)
        conn.commit()
        conn.close()
        
    def update_week(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE week SET 
                    runner_id = {self.runner_id},
                    total_distance = {self.total_distance},
                    hard_distance = {self.hard_distance},
                    easy_distance = {self.easy_distance},
                    session_count = {self.session_count},
                    hard_pace = {self.hard_pace},
                    run_count = {self.run_count},
                    days = '{json.dumps(self.days)}',
                    hard_time = {self.hard_time},
                    easy_pace = {self.easy_pace},
                    easy_time = {self.easy_time}
                    WHERE week = '{self.week}'
                    """)
        conn.commit()
        conn.close()