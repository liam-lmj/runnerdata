import sqlite3
from constants import run_types

class Gear:
    def __init__(self, name, runner, distance, active, default_type, gear_id=None):
        self.gear_id = gear_id
        self.name = name
        self.runner = runner
        self.distance = distance
        self.active = active
        self.default_type = default_type
    
    def gear_exists(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM gear WHERE week = '{self.gear_id}'")
        exists = c.fetchone()
        conn.close()
        if exists:
            return True
        else:
            return False
        
    def insert_gear(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO gear (name, runner, distance, active, default_type)
            VALUES (?, ?, ?, ?, ?)
        """, (self.name, self.runner, self.distance, self.active, self.default_type))
        conn.commit()
        gear_id = c.lastrowid
        conn.close()
        self.gear_id = gear_id
        self.check_and_clear_type_for_other_gear()
        return gear_id
            
    def update_gear(self):
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE gear SET 
                    name = '{self.name}', 
                    runner = '{self.runner}', 
                    distance = {self.distance}, 
                    active = '{self.active}', 
                    default_type = '{self.default_type}' 
                    WHERE gear_id = {self.gear_id}
                    """)
        conn.commit()
        conn.close()
        self.check_and_clear_type_for_other_gear()

    def check_and_clear_type_for_other_gear(self):
        if not self.default_type in run_types:
            return 
        conn = sqlite3.connect('runner.db')
        c = conn.cursor()
        c.execute(f"""UPDATE gear SET 
                    default_type = 'None' 
                    WHERE (gear_id != {self.gear_id}) AND (default_type = '{self.default_type}') AND (runner = '{self.runner}')
                    """)
        conn.commit()
        conn.close()


