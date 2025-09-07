import sqlite3
import json
from decimal import Decimal

class Plan:
    def __init__(self, request):
        self.week = request["week"]
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
        self.sessions = json.dumps(request["sessionsArray"])

    def parse_float(self, check):
        try:
            return float(check)
        except ValueError:
            return 0


    def plan_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM plan WHERE week = '{self.week}'")
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
            INSERT INTO plan (week, runner, monday, tuesday, wednesday, thursday, friday, saturday, sunday, total, current, achieved, sessions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                self.sessions
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
                        sessions = '{self.sessions}'
                    WHERE week = '{self.week}'
                    """)
        conn.commit()
        conn.close()
    

    
    