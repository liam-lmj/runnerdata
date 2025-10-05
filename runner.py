import sqlite3
from datetime import datetime

class Runner:
    def __init__(self, id):
        self.id = id
        if self.runner_exists():
            runner = self.load_from_database()[0]
            self.total_distance = runner["total_distance"]
            self.latest_activity = runner["latest_Activity"]
            self.refresh_token = runner["refresh_token"]
        else:
            self.total_distance = 0
            self.latest_activity = None
            self.refresh_token = None
    
    def add_activities(self, activities):
        latest_activity = self.latest_activity
        for activity in activities:
            self.total_distance += activity.easy_distance
            self.total_distance += activity.hard_distance
            if (latest_activity is None) or (type(latest_activity) == str) or (activity.date > latest_activity):
                latest_activity = activity.date
        self.latest_activity = latest_activity

    def runner_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM runner WHERE id = {self.id}")
        exists = c.fetchone()
        conn.close()
        if exists:
            return True
        else:
            return False

    def insert_runner(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO runner VALUES ({self.id}, {self.total_distance}, '{self.latest_activity}', '{self.refresh_token}')")
        conn.commit()
        conn.close()
    
    def update_runner(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE runner SET total_distance = {self.total_distance}, latest_Activity = '{self.latest_activity}', refresh_token = '{self.refresh_token}'
                WHERE id = {self.id}
                  """)
        conn.commit()
        conn.close()

    def load_from_database(self):
        conn = sqlite3.connect('runner.db')
        conn.row_factory = sqlite3.Row  
        c = conn.cursor()
        c.execute(f"SELECT * FROM runner WHERE id = {self.id}")
        runner = c.fetchall()
        conn.close()
        return runner
        

