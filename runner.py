import sqlite3
from datetime import datetime

class Runner:
    def __init__(self, id, total_distance, latest_activity, refresh_token):
        self.id = id
        self.total_distance = total_distance
        self.latest_activity = datetime.strptime(latest_activity, "%Y-%m-%d %H:%M:%S") #sqllite doesn't support dates so need to convert for class
        self.refresh_token = refresh_token
    
    def add_activities(self, activities):
        latest_activity = self.latest_activity
        for activity in activities:
            self.total_distance += activity.easy_distance
            self.total_distance += activity.hard_distance            
            if latest_activity is None or activity.date > latest_activity:
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


        

