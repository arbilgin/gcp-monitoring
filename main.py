from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # data = [
    #     {
    #         "machine_name": "greenlink-pod-XXXX",
    #         "environment": "staging" or "None",
    #         "cpu_limit": "8",
    #         "cpu_usage": "3.41",
    #         "memory_limit": "16",
    #         "memory_usage": "11.23",
    #     }
    # ]
    data = get_metrics():
    return render_template("index.html", response=data)


if __name__ == "__main__":
    app.run(debug=True)
