from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

from pathlib import Path

import pandas as pd

from extractors.electric import extract_electric_bill
from extractors.electric import create_pretty_excel
from extractors.electric import OUTPUT_FILE


# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

Path("uploads").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")

def home():

    return render_template("index.html")


# =========================================================
# UPLOAD + PROCESS
# =========================================================

@app.route("/upload", methods=["POST"])

def upload_files():

    uploaded_files = request.files.getlist("files")

    if not uploaded_files:

        return "No files uploaded."

    all_rows = []

    uploads_folder = Path("uploads")

    # -----------------------------------------------------
    # SAVE + PROCESS FILES
    # -----------------------------------------------------

    for file in uploaded_files:

        if file.filename == "":

            continue

        if not file.filename.lower().endswith(".pdf"):

            continue

        filepath = uploads_folder / file.filename

        file.save(filepath)

        extracted_rows = extract_electric_bill(filepath)

        all_rows.extend(extracted_rows)

    # -----------------------------------------------------
    # NO DATA CHECK
    # -----------------------------------------------------

    if len(all_rows) == 0:

        return "No bill data could be extracted."

    # -----------------------------------------------------
    # CREATE DATAFRAME
    # -----------------------------------------------------

    df = pd.DataFrame(all_rows)

    # -----------------------------------------------------
    # CREATE EXCEL
    # -----------------------------------------------------

    create_pretty_excel(df)

    # -----------------------------------------------------
    # DOWNLOAD FILE
    # -----------------------------------------------------

    return send_file(
        OUTPUT_FILE,
        as_attachment=True
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
    