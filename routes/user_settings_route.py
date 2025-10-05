from flask import Blueprint, render_template, redirect, session, request, jsonify

setting_bp = Blueprint('settings_bp', __name__)

@setting_bp.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("settings.html")