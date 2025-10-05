import sqlite3
import json
from datetime import datetime, timedelta 
from constants import mile_conversion

class Plan:
    def __init__(self, request):
        self.week = request["weekNewPlan"]
        self.monday = self.parse_float(request["monday"])
        self.tuesday = self.parse_float(request["tuesday"])
        self.wednesday = self.parse_float(request["wednesday"])
        self.thursday = self.parse_float(request["thursday"])
        self.friday = self.parse_float(request["friday"])
        self.saturday = self.parse_float(request["saturday"])
        self.sunday = self.parse_float(request["sunday"])
        self.total = self.parse_float(request["total"])
        self.runner = request["runner"]
        self.achieved = request["achieved"]
        self.current = request["current"]
        self.sessions = json.dumps(request["sessions"])
        self.real_session_count = 0
        self.real_miles = 0

    def parse_float(self, check):
        try:
            return float(check)
        except ValueError:
            return 0

    def plan_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM plan WHERE week = '{self.week}' and runner = {self.runner}")
        exists = c.fetchone()
        conn.close()
        if exists:
            return True
        else:
            return False
        
    def insert_plan(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO plan (week, runner, monday, tuesday, wednesday, thursday, friday, saturday, sunday, total, current, achieved, sessions, real_miles, real_session_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.week,
                self.runner,
                self.monday,
                self.tuesday,
                self.wednesday,
                self.thursday,
                self.friday,
                self.saturday,
                self.sunday,
                self.total,
                self.current,
                self.achieved,
                self.sessions,
                self.real_miles,
                self.real_session_count
            ))
        conn.commit()
        conn.close()
        
    def update_plan(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE plan SET 
                        monday = {self.monday}, 
                        tuesday = {self.tuesday}, 
                        wednesday = {self.wednesday}, 
                        thursday = {self.thursday}, 
                        friday = {self.friday}, 
                        saturday = {self.saturday}, 
                        sunday = {self.sunday}, 
                        total = {self.total}, 
                        current = '{self.current}', 
                        achieved = '{self.achieved}', 
                        sessions = '{self.sessions}',
                        real_miles = {self.real_miles},
                        real_session_count = {self.real_session_count}
                    WHERE week = '{self.week}'
                    """)
        conn.commit()
        conn.close()
    
    def update_current(self):
        week_date = datetime.strptime(f"{self.week}-1 00:00:00", "%W-%Y-%w %H:%M:%S")
        end_week = week_date + timedelta(days=7)
        now = datetime.now()
        if now < end_week:
            self.current = "true"
        else:
            self.current = "false"

    def compare_vs_week(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT total_distance, session_count FROM week WHERE week = '{self.week}'")
        week = c.fetchone()
        conn.close()
        if week:
            return week
        else:
            return False
        
    def update_vs_week(self):
        real_week = self.compare_vs_week()
        if not real_week:
            return
        real_distance = round(real_week[0] / mile_conversion,2) #array order comes from sql series in compare_vs_week
        real_session_count = real_week[1] 
        self.real_miles = real_distance
        self.real_session_count = real_session_count
        if self.total <= self.real_miles:
            self.achieved = "true"
        elif self.current == "false":
            self.achieved = "false"
        else:
            self.achieved = "pending"