import re
from datetime import datetime, timedelta

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_date_range(start_date: str, end_date: str) -> list[str]:
    errors = []
    if not start_date or not DATE_RE.match(start_date):
        errors.append("startDate must be in YYYY-MM-DD format")
    if not end_date or not DATE_RE.match(end_date):
        errors.append("endDate must be in YYYY-MM-DD format")
    if errors:
        return errors

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        errors.append("startDate is not a valid date")
        start = None
    try:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        errors.append("endDate is not a valid date")
        end = None
    if errors:
        return errors

    if start > end:
        errors.append("startDate must be on or before endDate")
    if end - start > timedelta(days=366):
        errors.append("Date range cannot exceed 1 year")

    return errors


def validate_location_query(location: str | None) -> list[str]:
    errors = []
    if not location or not location.strip():
        errors.append("location is required")
    elif len(location.strip()) > 200:
        errors.append("location is too long")
    return errors
