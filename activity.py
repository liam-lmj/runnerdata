import sqlite3
from constants import session_pace

class Activity:
    def __init__(self, activity):
        self.activity_id = activity["activity_id"]
        self.runner = activity["runner"]
        self.date = activity["date"]
        laps = activity["laps"]
        self.set_up_lap_attributes(laps)
    
    def set_up_lap_attributes(self, laps):
        count_of_reps = 0
        rep_pace_sum = 0
        hard_distance = 0
        easy_distance = 0
        rep_pace = 0
        run_type = None
        for lap in laps:
            pace = lap["speed"]
            distance = lap["distance"]
            if pace < session_pace:
                count_of_reps += 1
                rep_pace_sum += pace
                hard_distance += distance
            else:
                easy_distance += distance
        if count_of_reps > 0:
            run_type = "Session"
            rep_pace = round(rep_pace_sum / count_of_reps, 2)
        else:
            run_type = "easy"
        self.count_of_reps = count_of_reps
        self.hard_distance = hard_distance
        self.rep_pace = rep_pace
        self.easy_distance = easy_distance
        self.run_type = run_type

    def activity_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM activity WHERE id = {self.activity_id}")
        exists = c.fetchone()
        conn.close()
        if exists:
            return True
        else:
            return False
    
    def insert_activity(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""INSERT INTO activity VALUES 
                  ({self.activity_id}, 
                  {self.runner}, 
                  '{self.date}',
                  '{self.run_type}',
                  {self.easy_distance + self.hard_distance},
                  {self.hard_distance},
                  {self.easy_distance},
                  {self.count_of_reps},
                  {self.rep_pace})""")
        conn.commit()
        conn.close()

    def update_activity(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE activity SET 
                    runner_id = {self.runner}, 
                    date = '{self.date}',
                    run_type = '{self.run_type}',
                    distance = {self.easy_distance + self.hard_distance},
                    easy_distance = {self.easy_distance},
                    hard_distance = {self.hard_distance},
                    rep_count = {self.count_of_reps},
                    rep_pace = {self.rep_pace}
                    WHERE id = {self.activity_id}
                    """)
        conn.commit()
        conn.close()
