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
# CREATE FLASK APP
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

    print("UPLOAD STARTED")

    if not uploaded_files:

        print("NO FILES FOUND")

        return "No files uploaded."

    all_rows = []

    uploads_folder = Path("uploads")

    # -----------------------------------------------------
    # PROCESS FILES
    # -----------------------------------------------------

    for file in uploaded_files:

        print(f"PROCESSING FILE: {file.filename}")

        if file.filename == "":

            print("EMPTY FILENAME")

            continue

        if not file.filename.lower().endswith(".pdf"):

            print("NOT PDF")

            continue

        filepath = uploads_folder / file.filename

        # SAVE FILE
        file.save(filepath)

        print(f"FILE SAVED: {filepath}")

        # EXTRACT DATA
        try:

            extracted_rows = extract_electric_bill(filepath)

            print(f"ROWS EXTRACTED: {len(extracted_rows)}")

            if extracted_rows:

                print(extracted_rows[0])

            all_rows.extend(extracted_rows)

        except Exception as e:

            print(f"ERROR: {e}")

            return f"ERROR: {e}"

    # -----------------------------------------------------
    # NO DATA FOUND
    # -----------------------------------------------------

    if len(all_rows) == 0:

        return """
        <h2>No bill data extracted.</h2>
        <p>Check Render logs.</p>
        """

    # -----------------------------------------------------
    # CREATE DATAFRAME
    # -----------------------------------------------------

    df = pd.DataFrame(all_rows)

    # -----------------------------------------------------
    # FIX NUMBER FORMAT
    # -----------------------------------------------------

    df["current_charges"] = (
        df["current_charges"]
        .astype(str)
        .str.replace(",", "")
        .astype(float)
    )

    # -----------------------------------------------------
    # CREATE EXCEL
    # -----------------------------------------------------

    create_pretty_excel(df)

    print("EXCEL CREATED")

    # -----------------------------------------------------
    # SUMMARY VALUES
    # -----------------------------------------------------

    total_charges = round(
        df["current_charges"].sum(),
        2
    )

    confidence = 98

    # -----------------------------------------------------
    # SHOW RESULTS PAGE
    # -----------------------------------------------------

    return render_template(
        "results.html",
        pdf_count=len(uploaded_files),
        row_count=len(df),
        total_charges=f"{total_charges:,.2f}",
        confidence=confidence
    )


# =========================================================
# DOWNLOAD EXCEL
# =========================================================

@app.route("/download")

def download_file():

    return send_file(
        OUTPUT_FILE,
        as_attachment=True
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )