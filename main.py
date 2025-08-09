import sqlite3
from datetime import datetime
from stravaapi import new_access_token, get_activities
from runner import Runner
from activity import Activity
from week import Week

def main():
    conn = sqlite3.connect('runner.db')
    conn.row_factory = sqlite3.Row  
    c = conn.cursor()
    c.execute("SELECT * FROM runner")
    runners = c.fetchall()
    conn.close()

    if len(runners) < 1:
        raise Exception("No runners found")
    
    for runner_data in runners:
        runner = Runner(runner_data["id"], runner_data["total_distance"], runner_data["latest_Activity"], runner_data["refresh_token"])

        access_token = new_access_token(runner.refresh_token)
        activities_json = get_activities(access_token)
        
        new_activities = []
        activity_weeks = set()

        for activity_dict in activities_json:
            activity = Activity(activity_dict)
            if not activity.activity_exists():
                activity.insert_activity()
                new_activities.append(activity)
                week_year = activity.date.strftime("%W-%Y")
                activity_weeks.add(week_year)

        runner.add_activities(new_activities)
        runner.update_runner()

        for week_year in activity_weeks:
            week = Week(week_year, runner.id)
            if week.week_exists():
                week.update_week()
            else:
                week.insert_week()

if __name__ == "__main__":
    main()