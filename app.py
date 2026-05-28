from flask import Flask
from flask import request
from flask import send_file
from pathlib import Path
import pandas as pd
import os

from extractors.electric import extract_electric_bill
from extractors.electric import create_pretty_excel
from extractors.electric import OUTPUT_FILE

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        </div>

        <div class="main">

            <div class="card">

                <h1>Billing Dashboard</h1>

                <p>

                    Utility billing management system.

                </p>

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

        <title>Tasks</title>

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

        </div>

        <div class="main">

            <h1>Tasks Dashboard</h1>

            <p>

                Future tasks and approvals will appear here.

            </p>

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
    <!DOCTYPE html>

    <html>

    <head>

        <title>Electric Bills</title>

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

            .upload-box {

                background: white;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                max-width: 700px;
            }

            .upload-button {

                padding: 14px 20px;
                background: #2563eb;
                border: none;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }

            .upload-button:hover {

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

        </div>

        <div class="main">

            <div class="upload-box">

                <h1>Electric Bill Upload</h1>

                <br>

                <form
                    action="/upload-electric"
                    method="POST"
                    enctype="multipart/form-data"
                >

                    <input
                        type="file"
                        name="files"
                        multiple
                        required
                    >

                    <br><br>

                    <button
                        class="upload-button"
                        type="submit"
                    >

                        Upload Bills

                    </button>

                </form>

            </div>

        </div>

    </body>

    </html>
    """


# =========================================================
# UPLOAD ELECTRIC
# =========================================================

@app.route("/upload-electric", methods=["POST"])
def upload_electric():

    uploaded_files = request.files.getlist("files")

    all_rows = []

    for file in uploaded_files:

        if file.filename == "":
            continue

        filepath = Path(UPLOAD_FOLDER) / file.filename

        file.save(filepath)

        try:

            extracted_rows = extract_electric_bill(filepath)

            all_rows.extend(extracted_rows)

        except Exception as e:

            print("ERROR:", e)

    if not all_rows:

        return """
        <h1>No bill data extracted.</h1>
        <br>
        <a href='/electric'>Back</a>
        """

    df = pd.DataFrame(all_rows)

    create_pretty_excel(df)

    return send_file(
        OUTPUT_FILE,
        as_attachment=True
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)