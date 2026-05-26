from pathlib import Path

import pandas as pd

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

from extractors.detector import detect_bill_type
from extractors.electric import extract_electric_bill
from extractors.electric import create_pretty_excel


app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_files():

    uploaded_files = request.files.getlist("pdf_files")

    all_rows = []

    total_files = 0

    failed_files = []

    warning_files = []

    for file in uploaded_files:

        if file.filename == "":
            continue

        total_files += 1

        save_path = UPLOAD_FOLDER / file.filename

        file.save(save_path)

        try:

            # -------------------------------------
            # DETECT BILL TYPE
            # -------------------------------------

            bill_type = detect_bill_type(save_path)

            # -------------------------------------
            # ELECTRIC EXTRACTION
            # -------------------------------------

            if bill_type == "Electric":

                extracted_rows = extract_electric_bill(save_path)

                # ---------------------------------
                # FAILED EXTRACTION
                # ---------------------------------

                if not extracted_rows:

                    failed_files.append({
                        "file": file.filename,
                        "reason": "No rows extracted"
                    })

                    continue

                # ---------------------------------
                # WARNING CHECKS
                # ---------------------------------

                for row in extracted_rows:

                    warnings = []

                    if "NOT FOUND" in str(row.get("account_number", "")):
                        warnings.append("Missing Account Number")

                    if "NOT FOUND" in str(row.get("billing_date", "")):
                        warnings.append("Missing Billing Date")

                    if "NOT FOUND" in str(row.get("service_address", "")):
                        warnings.append("Missing Address")

                    if "NOT FOUND" in str(row.get("current_charges", "")):
                        warnings.append("Missing Charges")

                    if warnings:

                        warning_files.append({
                            "file": file.filename,
                            "warnings": ", ".join(warnings)
                        })

                all_rows.extend(extracted_rows)

            else:

                failed_files.append({
                    "file": file.filename,
                    "reason": f"Unsupported bill type: {bill_type}"
                })

        except Exception as error:

            failed_files.append({
                "file": file.filename,
                "reason": str(error)
            })

    # -----------------------------------------
    # CREATE DATAFRAME
    # -----------------------------------------

    df = pd.DataFrame(all_rows)

    # -----------------------------------------
    # CREATE EXCEL
    # -----------------------------------------

    if not df.empty:

        create_pretty_excel(df)

    # -----------------------------------------
    # SUMMARY STATS
    # -----------------------------------------

    total_rows = len(df)

    missing_account_numbers = 0
    missing_dates = 0
    missing_addresses = 0
    missing_charges = 0

    if not df.empty:

        missing_account_numbers = (
            df["account_number"]
            .astype(str)
            .str.contains("NOT FOUND", case=False)
            .sum()
        )

        missing_dates = (
            df["billing_date"]
            .astype(str)
            .str.contains("NOT FOUND", case=False)
            .sum()
        )

        missing_addresses = (
            df["service_address"]
            .astype(str)
            .str.contains("NOT FOUND", case=False)
            .sum()
        )

        missing_charges = (
            df["current_charges"]
            .astype(str)
            .str.contains("NOT FOUND", case=False)
            .sum()
        )

    return render_template(
        "index.html",
        uploaded_files=all_rows,
        excel_ready=True,
        total_files=total_files,
        total_rows=total_rows,
        missing_account_numbers=missing_account_numbers,
        missing_dates=missing_dates,
        missing_addresses=missing_addresses,
        missing_charges=missing_charges,
        failed_files=failed_files,
        warning_files=warning_files,
    )


@app.route("/download")
def download_excel():

    return send_file(
        "outputs/output.xlsx",
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(debug=True)