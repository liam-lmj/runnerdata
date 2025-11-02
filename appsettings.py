from flask import session, jsonify
from runner import Runner

def update_settings(request):
    unit = request["unit"]
    method = request["method"]
    lt2 = request["lt2"]
    lt1 = request["lt1"]
    hard = request["hard"]

    runner_id = session['user_id']
    runner = Runner(runner_id)
    runner.update_runner_settings(unit, method, lt1, lt2, hard)

    return jsonify({"success": True })