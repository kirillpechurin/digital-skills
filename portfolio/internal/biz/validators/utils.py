from datetime import date


def date_validate(value):
    try:
        date.fromisoformat(str(value))
    except:
        raise TypeError("некорректная дата")
