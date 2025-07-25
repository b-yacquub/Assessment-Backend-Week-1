"""Functions for working with dates."""

from datetime import datetime, date, timedelta
import math


def convert_to_datetime(date_val: str) -> datetime:
    try:
        return datetime.strptime(date_val, '%d.%m.%Y')
    except ValueError:
        raise ValueError("Unable to convert value to datetime.")


def get_days_between(first: datetime, last: datetime) -> int:

    if not isinstance(first, datetime) or not isinstance(last, datetime):
        raise TypeError("Datetimes required.")
    return (last-first).days


def get_day_of_week_on(date_val: datetime) -> str:
    if not isinstance(date_val, datetime):
        raise TypeError("Datetime required.")

    return date_val.__format__('%A')


def get_current_age(birthdate: date) -> int:
    if not isinstance(birthdate, date):
        raise TypeError('Date required.')
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age
