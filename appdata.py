from datetime import datetime, timedelta
from constants import days_in_week, week_order, days_of_week

def current_week_year():
    now = datetime.now()
    week_year = now.strftime("%W-%Y")
    return week_year

def get_next_five_weeks():
    next_five_weeks = []

    date = datetime.now()
    for i in range(1,6):
        date += timedelta(days=7)
        week_year = date.strftime("%W-%Y")
        next_five_weeks.append(week_year)

    return next_five_weeks

def get_weekly_mileage(week_data):
    weekly_mileage = []

    for week in week_data:
        days = week["days"]
        days_dict = eval(days)
        sorted_dict = {}
        total_distance = 0
        easy_distance = 0
        hard_distance = 0
        hard_time = 0 
        hard_pace = 0
        for day in week_order:
            if day in days_dict:
                sorted_dict[days_of_week[day]] = days_dict[day]
                total_distance += days_dict[day]["total_distance"]
                easy_distance += days_dict[day]["easy_distance"]
                hard_distance += days_dict[day]["hard_distance"]
                hard_time += days_dict[day]["hard_distance"] * days_dict[day]["hard_pace"]

        if hard_distance > 0:
            hard_pace = round((hard_time / hard_distance), 2)
        
        sorted_dict["Total"] = {"total_distance": total_distance, 
                                "easy_distance": easy_distance,
                                "hard_distance": hard_distance,
                                "hard_pace": hard_pace}

        if len(days_dict) == days_in_week:
            sorted_dict["week"] = week["week"]
            weekly_mileage.append(sorted_dict)

    weekly_mileage.reverse()    

    return weekly_mileage