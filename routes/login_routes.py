from flask import Blueprint, render_template, redirect, session, request
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
    access_token = new_access_token(refresh_token)
    activity_list = get_activities(access_token)
    session['user_id'] = runner_id
    return redirect("/dash")