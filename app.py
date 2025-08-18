from flask import Flask, render_template
from dashboard import init_dashboard

app = Flask(__name__)

init_dashboard(app)

@app.route("/")
def home():
    return "<h1>Welcome to the running data app</h1><p>Go to: <a href='/dash/'>Runner Data!</a></p>"

if __name__ == "__main__":
    app.run(debug=True)