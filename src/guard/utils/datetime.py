from datetime import UTC, datetime, timedelta, timezone


def get_now(tz: timezone | None = UTC) -> datetime:
    return datetime.now(tz)


def get_default_expires_at(
    timedelta_seconds: int, tz: timezone | None = UTC
) -> datetime:
    return get_now(tz) + timedelta(seconds=timedelta_seconds)
