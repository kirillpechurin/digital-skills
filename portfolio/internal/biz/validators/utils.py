from datetime import date, datetime
from calendar import Calendar


def date_validate(value):
    try:
        date.fromisoformat(str(value))
    except:
        raise TypeError("некорректная дата")


def get_calendar():
    month_str = datetime.now().strftime("%B")
    day, month, year = datetime.now().day, datetime.now().month, datetime.now().year
    calendar = Calendar().monthdatescalendar(year, month)
    return calendar, month_str
