import pdfplumber


# =========================================================
# READ PDF TEXT
# =========================================================

def extract_text(filepath):

    text_parts = []

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            text = page.extract_text() or ""

            text_parts.append(text.lower())

    return "\n".join(text_parts)


# =========================================================
# DETECT BILL TYPE
# =========================================================

def detect_bill_type(filepath):

    text = extract_text(filepath)

    # -----------------------------------------------------
    # ELECTRIC
    # -----------------------------------------------------

    if (
        "current charges" in text
        or "kwh" in text
        or "electric" in text
    ):

        return "electric"

    # -----------------------------------------------------
    # WATER
    # -----------------------------------------------------

    if (
        "water usage" in text
        or "gallons" in text
        or "water bill" in text
    ):

        return "water"

    # -----------------------------------------------------
    # GAS
    # -----------------------------------------------------

    if (
        "therms" in text
        or "natural gas" in text
        or "gas service" in text
    ):

        return "gas"

    # -----------------------------------------------------
    # PHONE
    # -----------------------------------------------------

    if (
        "wireless" in text
        or "mobile" in text
        or "phone number" in text
    ):

        return "phone"

    # -----------------------------------------------------
    # INTERNET
    # -----------------------------------------------------

    if (
        "internet" in text
        or "broadband" in text
        or "wifi" in text
    ):

        return "internet"

    # -----------------------------------------------------
    # SEWER
    # -----------------------------------------------------

    if "sewer" in text:

        return "sewer"

    # -----------------------------------------------------
    # TRASH
    # -----------------------------------------------------

    if (
        "trash" in text
        or "solid waste" in text
        or "recycling" in text
    ):

        return "trash"

    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    return "electric"