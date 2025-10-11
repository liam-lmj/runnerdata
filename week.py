import sqlite3
import json
from datetime import datetime, timedelta
from constants import min_miles_conversion, week_order

class Week:
    def __init__(self, week, runner_id):
        self.week = week
        self.runner_id = runner_id
        self.total_distance = 0
        self.hard_distance = 0
        self.easy_distance = 0
        self.session_count = 0
        self.run_count = 0
        self.hard_pace = 0
        self.hard_time = 0
        self.easy_time = 0
        self.easy_pace = 0
        self.days = {}
        self.set_up_total_attributes()

    def get_activities(self):
        week_start = datetime.strptime(f"{self.week}-1 00:00:00", "%W-%Y-%w %H:%M:%S")
        week_end = week_start + timedelta(days=7)

        conn = sqlite3.connect('runner.db')
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()
                
        c.execute("""
            SELECT
                date,
                run_type,
                COALESCE(easy_distance, 0) AS easy_distance,
                COALESCE(easy_time, 0) AS easy_time,
                COALESCE(hard_distance, 0) AS hard_distance,
                COALESCE(hard_time, 0) AS hard_time,
                COALESCE(lt1_distance, 0) AS lt1_distance,
                COALESCE(lt1_time, 0) AS lt1_time,
                COALESCE(lt2_distance, 0) AS lt2_distance,
                COALESCE(lt2_time, 0) AS lt2_time,
                COALESCE(hard_reps_long_distance, 0) AS hard_reps_long_distance,
                COALESCE(hard_reps_long_time, 0) AS hard_reps_long_time,
                COALESCE(hard_reps_short_distance, 0) AS hard_reps_short_distance,
                COALESCE(hard_reps_short_time, 0) AS hard_reps_short_time
            FROM activity
            WHERE runner_id = ?
            AND date BETWEEN ? AND ?
        """, (self.runner_id, week_start, week_end))

        activities = c.fetchall()

        conn.commit()
        conn.close()

        return activities

    def set_up_total_attributes(self):
        activities = self.get_activities()
        days = {}

        for day in week_order:
            default_values = {
                "hard_distance": 0,
                "easy_distance": 0,
                "total_distance": 0,
                "hard_time": 0,
                "count_of_runs": 0,
                "count_of_sessions": 0,
                "hard_pace": 0,
                "lt1_time": 0,
                "lt1_pace": 0,
                "lt1_distance": 0,
                "lt2_time": 0,
                "lt2_pace": 0,
                "lt2_distance": 0,
                "hard_reps_short_time": 0,
                "hard_reps_short_pace": 0,
                "hard_reps_short_distance": 0,
                "hard_reps_long_time": 0,
                "hard_reps_long_pace": 0,
                "hard_reps_long_distance": 0
            }
            days[day] = default_values


        for activity in activities:
            date_string = activity["date"]
            date_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            date_day = date_datetime.strftime("%w")

            run_type = activity["run_type"]

            easy_distance = activity["easy_distance"]
            easy_time = activity["easy_time"]

            hard_distance = activity["hard_distance"]
            hard_time = activity["hard_time"]

            lt1_distance = activity["lt1_distance"]
            lt1_time = activity["lt1_time"]

            lt2_distance = activity["lt2_distance"]
            lt2_time = activity["lt2_time"]

            hard_reps_long_distance = activity["hard_reps_long_distance"]
            hard_reps_long_time = activity["hard_reps_long_time"]

            hard_reps_short_distance = activity["hard_reps_short_distance"] 
            hard_reps_short_time = activity["hard_reps_short_time"] 

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

                days[date_day]["lt1_distance"] += lt1_distance
                days[date_day]["lt2_distance"] += lt2_distance
                days[date_day]["hard_reps_long_distance"] += hard_reps_long_distance
                days[date_day]["hard_reps_short_distance"] += hard_reps_short_distance

                days[date_day]["lt1_time"] += lt1_time
                days[date_day]["lt2_time"] += lt2_time
                days[date_day]["hard_reps_long_time"] += hard_reps_long_time
                days[date_day]["hard_reps_short_time"] += hard_reps_short_time

                days[date_day]["hard_time"] += hard_time
                
                days[date_day]["count_of_runs"] += 1
                if run_type == "Session":
                    days[date_day]["count_of_sessions"] += 1
                    if hard_time > 0 and hard_distance > 0:
                        days[date_day]["hard_pace"] = round(min_miles_conversion / (days[date_day]["hard_distance"] / days[date_day]["hard_time"]), 2)

                    if lt1_time is not None and lt1_time > 0 and lt1_distance > 0:
                        days[date_day]["lt1_pace"] = round(min_miles_conversion / (days[date_day]["lt1_distance"] / days[date_day]["lt1_time"]), 2)

                    if lt2_time is not None and lt2_time > 0 and lt2_distance > 0:
                        days[date_day]["lt2_pace"] = round(min_miles_conversion / (days[date_day]["lt2_distance"] / days[date_day]["lt2_time"]), 2)

                    if hard_reps_long_time is not None and hard_reps_long_time > 0 and hard_reps_long_distance > 0:
                        days[date_day]["hard_reps_long_pace"] = round(min_miles_conversion / (days[date_day]["hard_reps_long_distance"] / days[date_day]["hard_reps_long_time"]), 2)

                    if hard_reps_short_time is not None and hard_reps_short_time > 0 and hard_reps_short_distance > 0:
                        days[date_day]["hard_reps_short_pace"] = round(min_miles_conversion / (days[date_day]["hard_reps_short_distance"] / days[date_day]["hard_reps_short_time"]), 2)
        
        if self.hard_distance > 0 and self.hard_time > 0:
            self.hard_pace = round(min_miles_conversion / (self.hard_distance / self.hard_time), 2)
        if self.easy_distance and self.easy_time > 0:
            self.easy_pace = round(min_miles_conversion / (self.easy_distance / self.easy_time), 2)
        self.days = days 

    def week_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM week WHERE week = '{self.week}' and runner_id = {self.runner_id}")
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
                  {self.easy_pace},
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