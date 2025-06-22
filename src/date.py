import datefinder
from datetime import datetime

def extract_date(text):
    matches = list(datefinder.find_dates(text))
    matches = [d for d in matches if d.year <= datetime.now().year]

    if matches:
        return matches[0].strftime("%Y-%m-%d")

    return "Unknown Date"