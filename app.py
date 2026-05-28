from flask import Flask

app = Flask(__name__)

# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Billing Dashboard</title>

        <style>

            body {

                margin: 0;
                font-family: Arial, sans-serif;
                display: flex;
                background: #f4f7fb;
            }

            .sidebar {

                width: 250px;
                min-height: 100vh;
                background: #0f172a;
                padding: 20px;
            }

            .sidebar h2 {

                color: white;
                margin-bottom: 30px;
            }

            .sidebar button {

                width: 100%;
                padding: 14px;
                margin-bottom: 12px;
                border: none;
                border-radius: 8px;
                background: #1e293b;
                color: white;
                cursor: pointer;
                font-size: 16px;
            }

            .sidebar button:hover {

                background: #334155;
            }

            .main {

                flex: 1;
                padding: 40px;
            }

            .card {

                background: white;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                max-width: 700px;
            }

        </style>

    </head>

    <body>

        <div class="sidebar">

            <h2>Billing Portal</h2>

            <button onclick="window.location.href='/'">

                Dashboard

            </button>

            <button onclick="window.location.href='/tasks'">

                Tasks

            </button>

            <button onclick="window.location.href='/electric'">

                Electric Bills

            </button>

            <button onclick="window.location.href='/water'">

                Water Bills

            </button>

            <button onclick="window.location.href='/gas'">

                Gas Bills

            </button>

            <button onclick="window.location.href='/phone'">

                Phone Bills

            </button>

            <button onclick="window.location.href='/reports'">

                Reports

            </button>

        </div>

        <div class="main">

            <div class="card">

                <h1>Billing Dashboard</h1>

                <br>

                <p>

                    Welcome to the utility billing management portal.

                </p>

                <br>

                <button onclick="alert('Dashboard Works')">

                    TEST BUTTON

                </button>

            </div>

        </div>

    </body>

    </html>
    """


# =========================================================
# TASKS PAGE
# =========================================================

@app.route("/tasks")
def tasks():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Tasks Dashboard</title>

        <style>

            body {

                margin: 0;
                font-family: Arial, sans-serif;
                display: flex;
                background: #f4f7fb;
            }

            .sidebar {

                width: 250px;
                min-height: 100vh;
                background: #0f172a;
                padding: 20px;
            }

            .sidebar h2 {

                color: white;
                margin-bottom: 30px;
            }

            .sidebar button {

                width: 100%;
                padding: 14px;
                margin-bottom: 12px;
                border: none;
                border-radius: 8px;
                background: #1e293b;
                color: white;
                cursor: pointer;
                font-size: 16px;
            }

            .sidebar button:hover {

                background: #334155;
            }

            .main {

                flex: 1;
                padding: 40px;
            }

            .task-card {

                background: white;
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                margin-bottom: 20px;
            }

            .task-card h3 {

                margin-top: 0;
            }

            .task-button {

                padding: 12px 18px;
                border: none;
                border-radius: 8px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }

            .task-button:hover {

                background: #1d4ed8;
            }

        </style>

    </head>

    <body>

        <div class="sidebar">

            <h2>Billing Portal</h2>

            <button onclick="window.location.href='/'">

                Dashboard

            </button>

            <button onclick="window.location.href='/tasks'">

                Tasks

            </button>

            <button onclick="window.location.href='/electric'">

                Electric Bills

            </button>

            <button onclick="window.location.href='/water'">

                Water Bills

            </button>

            <button onclick="window.location.href='/gas'">

                Gas Bills

            </button>

            <button onclick="window.location.href='/phone'">

                Phone Bills

            </button>

            <button onclick="window.location.href='/reports'">

                Reports

            </button>

        </div>

        <div class="main">

            <h1>Tasks Dashboard</h1>

            <br>

            <div class="task-card">

                <h3>Review High Electric Bill</h3>

                <p>

                    Charges exceeded monthly average.

                </p>

                <button
                    class="task-button"
                    onclick="alert('Task Opened')"
                >

                    Review Task

                </button>

            </div>

            <div class="task-card">

                <h3>Missing Water Account Number</h3>

                <p>

                    Manual review required for extraction.

                </p>

                <button
                    class="task-button"
                    onclick="alert('Opening Review')"
                >

                    Open Review

                </button>

            </div>

        </div>

    </body>

    </html>
    """


# =========================================================
# ELECTRIC PAGE
# =========================================================

@app.route("/electric")
def electric():

    return """
    <h1 style="font-family: Arial; padding: 40px;">

        Electric Bills Page

    </h1>
    """


# =========================================================
# WATER PAGE
# =========================================================

@app.route("/water")
def water():

    return """
    <h1 style="font-family: Arial; padding: 40px;">

        Water Bills Page

    </h1>
    """


# =========================================================
# GAS PAGE
# =========================================================

@app.route("/gas")
def gas():

    return """
    <h1 style="font-family: Arial; padding: 40px;">

        Gas Bills Page

    </h1>
    """


# =========================================================
# PHONE PAGE
# =========================================================

@app.route("/phone")
def phone():

    return """
    <h1 style="font-family: Arial; padding: 40px;">

        Phone Bills Page

    </h1>
    """


# =========================================================
# REPORTS PAGE
# =========================================================

@app.route("/reports")
def reports():

    return """
    <h1 style="font-family: Arial; padding: 40px;">

        Reports Page

    </h1>
    """


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)