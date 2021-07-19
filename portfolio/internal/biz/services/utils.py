import string
from datetime import datetime
from random import choice, randint
from string import digits


def get_datetime_diff(datetime1: datetime, datetime2: datetime) -> float:
    """Разница в секундах между двумя datetime"""
    timestamp1 = datetime1.timestamp()
    timestamp2 = datetime2.timestamp()
    return timestamp1 - timestamp2


def get_passed_time(last_datetime: datetime) -> float:
    """Разница в секундах между указанным datetime и текущим"""
    today_datetime = datetime.today()
    return get_datetime_diff(today_datetime, last_datetime)


def get_random_code(length=6) -> str:
    return ''.join(choice(digits) for _ in range(length))


def get_temp_password() -> str:
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = randint(8, 15)
    return ''.join(choice(chars) for x in range(size))
