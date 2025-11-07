import pandas as pd
from flask import Blueprint, render_template, redirect, session, request, jsonify
from database import get_plan_data, get_runner_zones
from plan import Plan
from appdata import bar_chart_plan, get_next_five_weeks
from appsettings import update_settings

next_five_weeks = get_next_five_weeks()

training_bp = Blueprint('training', __name__)

@training_bp.route("/training", methods=["GET", "POST"])
def trainingplan():
    if not 'user_id' in session:
        return redirect("/")
    runner = session['user_id']
    unit, method, lt1, lt2, hard = get_runner_zones(runner)
    training_plans = get_plan_data(runner)
    df_plans = pd.DataFrame(get_plan_data(runner)) if training_plans else None
    inital_week = df_plans['week'].iloc[0] if training_plans else None

    bar_json_plans = bar_chart_plan(inital_week, df_plans) if training_plans else None

    if request.method == "POST": 
        if request.json["type"] == "Settings":
            return update_settings(request.json)
        elif request.json["type"] == "addPlan":
            plan = Plan(request.json)
            if plan.plan_exists():
                plan.update_plan()
                plan.update_vs_week()
            else:
                plan.insert_plan()
            training_plans = get_plan_data(runner)
            return jsonify({"success": True, "training_plans": training_plans})
        elif request.json["type"] == "updateChart":
            week = request.json["selectedWeek"]
            bar_json_plans = bar_chart_plan(week, df_plans)
            return jsonify({"success": True, "bar_json": bar_json_plans})

    return render_template("training.html", 
                           training_plans=training_plans, 
                           bar_json_plans=bar_json_plans,
                           current_week=inital_week, 
                           next_five_weeks=next_five_weeks, 
                           runner=runner, 
                           unit=unit, 
                           method=method, 
                           lt1=lt1, 
                           lt2=lt2, 
                           hard=hard) 
