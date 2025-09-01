import sqlite3
import json
from decimal import Decimal

class Plan:
    def __init__(self, plan_dict):
        self.week = plan_dict["Week"]
        self.monday = self.create_day("Monday", plan_dict)
        self.tuesday = self.create_day("Tuesday", plan_dict)
        self.wednesday = self.create_day("Wednesday", plan_dict)
        self.thursday = self.create_day("Thursday", plan_dict)
        self.friday = self.create_day("Friday", plan_dict)
        self.saturday = self.create_day("Saturday", plan_dict)
        self.sunday = self.create_day("Sunday", plan_dict)

    def create_day(self, day, plan_dict):
        easy_distance = Decimal(plan_dict[day + "_easy_distance"])
        hard_distance = Decimal(plan_dict[day + "_hard_distance"])
        total_distance = easy_distance + hard_distance
        return {"day": day, "easy_distance": str(easy_distance), "hard_distance": str(hard_distance), "total_distance": str(total_distance)}
    
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
        c.execute(f"""INSERT INTO plan VALUES 
                  ('{self.week}', 
                  '{json.dumps(self.monday)}', 
                  '{json.dumps(self.tuesday)}', 
                  '{json.dumps(self.wednesday)}', 
                  '{json.dumps(self.thursday)}', 
                  '{json.dumps(self.friday)}', 
                  '{json.dumps(self.saturday)}', 
                  '{json.dumps(self.sunday)}')
                  """)
        conn.commit()
        conn.close()
        
    def update_plan(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE plan SET 
                  monday = '{json.dumps(self.monday)}', 
                  tuesday = '{json.dumps(self.tuesday)}', 
                  wednesday = '{json.dumps(self.wednesday)}', 
                  thursday = '{json.dumps(self.thursday)}', 
                  friday = '{json.dumps(self.friday)}', 
                  saturday = '{json.dumps(self.saturday)}', 
                  sunday = '{json.dumps(self.sunday)}'
                    WHERE week = '{self.week}'
                    """)
        conn.commit()
        conn.close()
    

    
    