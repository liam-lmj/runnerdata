from flask import Blueprint, render_template, redirect, session, request, jsonify
from database import get_running_gear, get_gear_by_id
from gear import Gear
from constants import run_types

gear_bp = Blueprint('gear', __name__)

@gear_bp.route("/gear", methods=["GET", "POST"])
def gear():
    if not 'user_id' in session:
        return redirect("/")
    runner = session['user_id']
    running_gear = get_running_gear(runner)
    if request.method == "POST":
        gear_updates = request.json
        if gear_updates["type"] == "Settings":
            unit = gear_updates["unit"]
            method = gear_updates["method"]
            lt2 = gear_updates["lt2"]
            lt1 = gear_updates["lt1"]
            hard = gear_updates["hard"]
            print(f"unit: {unit} method: {method} lt2: {lt2} lt1: {lt1} hard: {hard}")

            return jsonify({"success": True })
        
        gear_id = None
        if gear_updates["type"] == "Update":
            total_new_miles = gear_updates["totalNewMiles"]
            gear_id = gear_updates["gear_id"]
            gear_data = get_gear_by_id(gear_id)

            deafultType = gear_updates["default_type"] if gear_updates["default_type"] in run_types else None
            active = gear_updates["active"]
            gear = Gear(gear_data["name"], 
                        gear_data["runner"], 
                        gear_data["distance"] + total_new_miles, 
                        active,
                        deafultType,
                        gear_id=gear_data["gear_id"])
            gear.update_gear()
        else:
            gear = Gear(gear_updates["trainer"],
                        runner,
                        float(gear_updates["miles"]),
                        "Active",
                        gear_updates["default_type"])
            gear_id = gear.insert_gear()

        return jsonify({"success": True, "gear_id": gear_id})
    return render_template("gear.html", running_gear=running_gear)