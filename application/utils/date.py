from datetime import datetime
from dateutil import tz


def convert_utc_to_asia_tz(utc_date: datetime):
    from_zone = tz.tzutc()
    to_zone = tz.gettz('Asia/Tashkent')
    utc = utc_date.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return local
