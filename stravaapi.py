import os
import requests
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from constants import runner_url, refresh_url, activities_url, laps_url_start, lap_url_end, page_limit, min_miles_conversion

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def load_runner(code):
    response = requests.post(runner_url, params={"client_id": client_id, "client_secret": client_secret, "code": code, "grant_type": "authorization_code"})
    if not response.ok:
        raise Exception("Failed get runner")
    response_json = response.json()
    refresh_token = response_json["refresh_token"]
    runner_id = response_json["athlete"]["id"]
    return refresh_token, runner_id

def new_access_token(refresh_token):
    response = requests.post(refresh_url, params={"client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token, "grant_type": "refresh_token"})
    if not response.ok:
        raise Exception("Failed to refresh token")
    response_json = response.json()
    access_token = response_json["access_token"]
    return access_token

def get_activities(access_token):
    response = requests.get(activities_url, params={"access_token": access_token, "per_page" : page_limit})
    if not response.ok:
        raise Exception("Failed to get activities data")
    response_json = response.json()
    activity_list = []
    for activity in response_json:
        activity_id = str(activity["id"])
        activity_type = str(activity["sport_type"])
        print(activity_exists(activity_id))
        print(activity_id)
        if activity_exists(activity_id):
            continue
        print(activity_type)
        if activity_type != "Run":
            continue
        activity_dict = {}
        date_string = activity["start_date"]
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        laps = get_activity_laps(access_token, activity_id)

        activity_dict["runner"] = activity["athlete"]["id"]
        activity_dict["activity_id"] = activity_id
        activity_dict["date"] = date
        activity_dict["laps"] = laps
        
        activity_list.append(activity_dict)
    return activity_list

def get_activity_laps(access_token, activity_id):
    laps_url = laps_url_start + activity_id + lap_url_end
    response = requests.get(laps_url, params={"access_token": access_token})
    if not response.ok:
        raise Exception("Failed to get lap data")
    response_json = response.json()
    lap_list = []
    for lap in response_json:
        lap_dict = {}
        speed = 0
        if lap["average_speed"] > 0:
            speed = round(min_miles_conversion / lap["average_speed"], 2)

        lap_dict["lap"] = lap["name"]
        lap_dict["distance"] = lap["distance"]
        lap_dict["moving_time"] = lap["moving_time"]
        lap_dict["speed"] = speed

        lap_list.append(lap_dict)
    return lap_list

def activity_exists(activity_id):
    conn = sqlite3.connect('runner.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM activity WHERE id = {activity_id}")
    exists = c.fetchone()
    conn.close()
    if exists:
        return True
    else:
        return False