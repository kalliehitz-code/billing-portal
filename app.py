from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from pathlib import Path

app = Flask(__name__)

# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Billing Dashboard</title>

    </head>

    <body style="font-family: Arial; padding: 40px;">

        <h1>BILLING DASHBOARD</h1>

        <br>

        <button onclick="window.location.href='/tasks'">

            GO TO TASKS

        </button>

    </body>

    </html>
    """


# =========================================================
# TASKS
# =========================================================

@app.route("/tasks")
def tasks():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Tasks Test</title>

    </head>

    <body style="font-family: Arial; padding: 40px;">

        <h1>TASKS PAGE</h1>

        <br>

        <button onclick="alert('WORKS')">

            CLICK ME

        </button>

        <br><br>

        <button onclick="window.location.href='/'">

            BACK TO DASHBOARD

        </button>

    </body>

    </html>
    """


# =========================================================
# PLACEHOLDER PAGES
# =========================================================

@app.route("/electric")
def electric():

    return "<h1>Electric Bills Page</h1>"


@app.route("/water")
def water():

    return "<h1>Water Bills Page</h1>"


@app.route("/gas")
def gas():

    return "<h1>Gas Bills Page</h1>"


@app.route("/phone")
def phone():

    return "<h1>Phone Bills Page</h1>"


@app.route("/reports")
def reports():

    return "<h1>Reports Page</h1>"


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)