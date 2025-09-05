#api fields

refresh_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
laps_url_start = "https://www.strava.com/api/v3/activities/"
lap_url_end = "/laps"

page_limit = 50 #number of new activities per runner
min_miles_conversion = 26.8224 #divide m/s by this to get minutes per mile

#activity fields

session_pace = 6 #should be attribute of runner to allow users with wider ranges of abilities

#app fields

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
