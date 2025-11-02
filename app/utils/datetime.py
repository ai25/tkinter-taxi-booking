from datetime import datetime


def format_datetime(date_str, time_str):
    if not date_str or not time_str:
        return None

    # Normalise time format to HH:MM
    hours, minutes = time_str.split(":")
    time_normalised = f"{int(hours):02d}:{int(minutes):02d}"

    datetime_str = f"{date_str} {time_normalised}"
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    return dt.strftime("%a, %b %d %Y, %H:%M")


def to_timestamp(date_str, time_str):
    if not date_str or not time_str:
        return None

    # Normalise time format to HH:MM
    hours, minutes = time_str.split(":")
    time_normalised = f"{int(hours):02d}:{int(minutes):02d}"

    datetime_str = f"{date_str} {time_normalised}"
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    return int(dt.timestamp())


def format_timestamp(ts: int):
    dt = datetime.fromtimestamp(float(ts))

    return dt.strftime("%a, %b %d %Y, %H:%M")


def timestamp_to_datetime(ts: int):
    return datetime.fromtimestamp(float(ts))
