from flask import Blueprint, render_template, redirect, session, request
from runner import Runner
from activity import Activity
from week import Week
from database import update_pending_plans
from constants import auth_url
from stravaapi import load_runner, new_access_token, get_activities

login_bp = Blueprint('login', __name__)

@login_bp.route("/")
def authorise():
    return render_template("authorise.html", auth_url=auth_url)

@login_bp.route("/loaduser")
def loaduser():
    code = request.args.get('code')

    refresh_token, runner_id = load_runner(code)
    session['user_id'] = runner_id
    runner = Runner(runner_id)

    if not runner.runner_exists():
        runner.insert_runner()

    access_token = new_access_token(refresh_token)
    activities_json = get_activities(access_token)
    print(access_token)

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

    update_pending_plans(runner.id)

    return redirect("/dash")

@login_bp.route("/demo")
def demo():
    session['user_id'] = 34892346
    return redirect("/dash")
