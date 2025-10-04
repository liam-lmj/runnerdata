from flask import Blueprint, render_template, redirect, session, request
from constants import auth_url
from stravaapi import load_runner

login_bp = Blueprint('login', __name__)

@login_bp.route("/")
def authorise():
    return render_template("authorise.html", auth_url=auth_url)

@login_bp.route("/loaduser")
def loaduser():
    code = request.args.get('code')
    refresh_token, runner_id = load_runner(code) 
    session['user_id'] = runner_id
    return redirect("/dash")