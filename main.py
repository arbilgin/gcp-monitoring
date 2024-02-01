import time

from flask import Flask, render_template, request, redirect, url_for
from google.cloud import monitoring_v3

from metrics import GoogleMetrics

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user"),
    "blokz": generate_password_hash("Monitor.123!")
}

session = { "logged_in": False }

def set_session(username):
    session["logged_in"] = True
    session["username"] = username
def setup_metrics():
    client = monitoring_v3.MetricServiceClient()
    project = f"projects/greenlink-platform-396912"
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 60 * 10},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        }
    )
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(time.time())},
            "start_time": {"seconds": int(time.time()) - 60 * 10},
        }
    )
    metrics = GoogleMetrics(client, project, aggregation, interval)
    return metrics

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
       username = request.form["username"]
       password = request.form["password"]
       if verify_password(username, password):
           set_session(username)
           return app.redirect("/")
       else:
           return "Invalid username or password", 401
    return render_template("login.html")

@auth.login_required
@app.route("/")
def index():
    if session["logged_in"] == True:
        metrics = setup_metrics()
        data = metrics.get_data()
        from pprint import pprint      
        pprint(data)
        return render_template("index.html", response=data)
    else:
        return redirect("/login")

if __name__ == "__main__":
     app.run(debug=True, port=5000, threaded=True, use_reloader=True)
