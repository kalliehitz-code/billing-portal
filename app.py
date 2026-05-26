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

    for file in uploaded_files:

        print(f"PROCESSING FILE: {file.filename}")

        if file.filename == "":

            print("EMPTY FILENAME")

            continue

        if not file.filename.lower().endswith(".pdf"):

            print("NOT PDF")

            continue

        filepath = uploads_folder / file.filename

        file.save(filepath)

        print(f"FILE SAVED: {filepath}")

        try:

            extracted_rows = extract_electric_bill(filepath)

            print(f"ROWS EXTRACTED: {len(extracted_rows)}")

            if extracted_rows:

                print(extracted_rows[0])

            all_rows.extend(extracted_rows)

        except Exception as e:

            print(f"ERROR: {e}")

            return f"ERROR: {e}"

    print(f"TOTAL ROWS: {len(all_rows)}")

    if len(all_rows) == 0:

        return """
        <h2>No bill data extracted.</h2>
        <p>Check Render logs.</p>
        """

    df = pd.DataFrame(all_rows)

    create_pretty_excel(df)

    print("EXCEL CREATED")

    return send_file(
        OUTPUT_FILE,
        as_attachment=True
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
    