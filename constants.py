import os
from dotenv import load_dotenv

#api fields
runner_url = "https://www.strava.com/oauth/token"
refresh_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
laps_url_start = "https://www.strava.com/api/v3/activities/"
lap_url_end = "/laps"

page_limit = 50 #number of new activities per runner
min_miles_conversion = 26.8224 #divide m/s by this to get minutes per mile

#activity fields
session_pace = 7 #should be attribute of runner to allow users with wider ranges of abilities
lt1_pace_zone = 7
lt2_pace_zone = 6.66
hard_pace_zone = 6.33
short_distance = 550
mile_conversion = 1609

#app fields
load_dotenv()
client_id = os.getenv("client_id")
redirect_uri = os.getenv("redirect_uri")
auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=read,activity:read_all&approval_prompt=force"

days_in_week = 7
week_order = ["1", "2", "3", "4", "5", "6", "0"]
days_of_week  = {
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "0": "Sunday"
}
run_types = ["Easy", "Hard"]
