import time
import os

from flask import Flask, render_template, request, redirect, url_for, session, make_response
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

session = { }

def set_session(username):
    session["logged_in"] = True
    session["username"] = username
    session["token"] = os.urandom(24).hex()  # Generates a random token
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

# @app.before_request
# def before_request():
#     if "token" in session:
#         token_cookie = request.cookies.get('session_token')
#         if token_cookie != session.get('token'):
#             # The session token cookie doesn't match the session token; log the user out
#             print ("token cookie: ", token_cookie)
#             print ("session token: ", session.get('token'))
#             session.clear()
#             return redirect("/login")

            
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
           response = make_response(redirect("/"))
           response.set_cookie('session_token', session['token'], secure=True, httponly=True)
           return response
        #    before_request()
       else:
           return "Invalid username or password", 401
       
    return render_template("login.html")

@auth.login_required
@app.route("/")
def index():
    token_cookie = request.cookies.get('session_token')
    if token_cookie == session.get('token'):
            metrics = setup_metrics()
            data = metrics.get_data()
            from pprint import pprint      
            pprint(data)
            return render_template("index.html", response=data)
    else:
        return redirect("/login")

if __name__ == "__main__":
     app.run(debug=True, port=5000, threaded=True, use_reloader=True)
