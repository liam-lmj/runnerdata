import sqlite3
from datetime import datetime
from constants import default_unit, default_type, hard_zone, lt1_zone, lt2_zone

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
            self.refresh_token = None #don't store refresh token for new runners anymore
    
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
        c.execute("""INSERT INTO runner (id, 
                                        total_distance, 
                                        latest_Activity, 
                                        refresh_token, 
                                        prefered_unit, 
                                        prefered_method, 
                                        lt1_zone, 
                                        lt2_zone, 
                                        hard_zone)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (
                      self.id,
                      self.total_distance,
                      self.latest_activity,
                      self.refresh_token,
                      default_unit,
                      default_type,
                      lt1_zone,
                      lt2_zone,
                      hard_zone
                  ))
        conn.commit()
        conn.close()
    
    def update_runner(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE runner SET total_distance = ?, 
                                        latest_Activity = ?, 
                                        refresh_token = ?
                    WHERE id = ?""", 
                    (
                        self.total_distance,
                        self.latest_activity,
                        self.refresh_token,
                        self.id
                    ))
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