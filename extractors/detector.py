import pdfplumber


def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    return text


def detect_bill_type(pdf_path):

    text = extract_text(pdf_path)

    # ---------------------------------
    # ELECTRIC
    # ---------------------------------

    electric_keywords = [
        "kwh",
        "kilowatt",
        "electric",
        "meter reading",
        "energy charge",
    ]

    # ---------------------------------
    # WATER
    # ---------------------------------

    water_keywords = [
        "water usage",
        "gallons",
        "sewer",
        "water service",
    ]

    # ---------------------------------
    # CELLULAR
    # ---------------------------------

    cellular_keywords = [
        "wireless",
        "mobile",
        "phone number",
        "device payment",
    ]

    # ---------------------------------
    # DETECTION
    # ---------------------------------

    for keyword in electric_keywords:

        if keyword in text:
            return "Electric"

    for keyword in water_keywords:

        if keyword in text:
            return "Water"

    for keyword in cellular_keywords:

        if keyword in text:
            return "Cellular"

    return "Unknown"
