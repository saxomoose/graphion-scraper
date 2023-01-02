import datetime
import os
import zoneinfo
import redis
from scraper import utils

logger = utils.get_logger(__name__)


def store(enterprise_number: int, json: str):
    seconds_until_end_of_day = _time_until_end_of_day().seconds
    client = redis.Redis(
        # host="localhost",
        host="redis",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )
    client.set(
        name=f"entity:{enterprise_number}", value=json, ex=seconds_until_end_of_day
    )


def _time_until_end_of_day():
    timezone = zoneinfo.ZoneInfo("Europe/Brussels")
    dt = datetime.datetime.now(tz=timezone)
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min, tzinfo=timezone) - dt
