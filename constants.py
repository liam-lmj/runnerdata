#api fields

refresh_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
laps_url_start = "https://www.strava.com/api/v3/activities/"
lap_url_end = "/laps"

page_limit = 10 #number of new activities per runner
min_miles_conversion = 26.8224 #divide m/s by this to get minutes per mile

#activity fields

session_pace = 7 #should be attribute of runner to allow users with wider ranges of abilities

