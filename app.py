import os
import pandas as pd 
from appdata import current_week_year
from flask import Flask, send_from_directory
from dashboard import init_dashboard
from database import get_week_data_all, get_days_day
from dotenv import load_dotenv
from routes.mileage_routes import mileage_log_bp
from routes.gear_route import gear_bp
from routes.training_route import training_bp
from routes.login_routes import login_bp
from routes.user_settings_route import setting_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

app.register_blueprint(mileage_log_bp)
app.register_blueprint(gear_bp)
app.register_blueprint(training_bp)
app.register_blueprint(login_bp)
app.register_blueprint(setting_bp)

current_week = current_week_year()
week_data = get_week_data_all()
df_days = pd.DataFrame(get_days_day(week_data))

init_dashboard(app, df_days)

#to deliver banner to dash app
@app.route("/bannerdash.html")
def serve_banner():
    return send_from_directory("templates", "bannerdash.html")

if __name__ == "__main__":
    app.run(debug=True)