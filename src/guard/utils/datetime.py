from datetime import datetime, timezone


def get_datetime_now(tz: timezone | None = None):
    return datetime.now(tz)
