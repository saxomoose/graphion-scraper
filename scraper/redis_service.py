import datetime
import os
import zoneinfo
import redis
from scraper import utils

logger = utils.get_logger(__name__)

# TTL set to seconds until end of day. Assumes that KBO data is refreshed at first interval after midnight.
def store(enterprise_number: int, json: str):
    seconds_until_end_of_day = time_until_end_of_day().seconds
    client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        username=os.getenv("REDIS_USER"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )
    client.set(
        name="{0}:legalperson:{1}".format(os.getenv("REDIS_USER"), enterprise_number), value=json, ex=seconds_until_end_of_day
    )
 
def time_until_end_of_day():
    timezone = zoneinfo.ZoneInfo("Europe/Brussels")
    dt = datetime.datetime.now(tz=timezone)
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min, tzinfo=timezone) - dt
