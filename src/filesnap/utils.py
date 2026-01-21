import time


def format_date(date: int | float) -> str:
    return str(time.ctime(date))
