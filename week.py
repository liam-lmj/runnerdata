import sqlite3
from datetime import datetime, timedelta

class Week:
    def __init__(self, week, runner_id):
        self.week = week
        self.runner_id = runner_id
        activities = self.get_activities(self.week)
        self.set_up_total_attributes(activities)


    def get_activities(self, week):
        week_start = datetime.strptime(f"{week}-1 00:00:00", "%W-%Y-%w %H:%M:%S")
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

    def set_up_total_attributes(self, activities):
        self.total_distance = 0
        self.hard_distance = 0
        self.easy_distance = 0
        self.session_count = 0
        self.hard_pace = 0
        total_pace = 0
        for activity in activities:
            self.total_distance += activity["distance"] 
            self.hard_distance += activity["hard_distance"] 
            self.easy_distance += activity["easy_distance"] 
            total_pace += activity["rep_pace"]
            if activity["run_type"] == "Session":
                self.session_count += 1
        if self.session_count > 0:
            self.hard_pace = total_pace / self.session_count

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
                  {self.hard_pace})
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
                    hard_pace = {self.hard_pace}
                    WHERE week = '{self.week}'
                    """)
        conn.commit()
        conn.close()