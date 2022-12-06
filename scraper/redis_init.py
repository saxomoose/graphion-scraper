import redis

from scraper import utils

logger = utils.get_logger(__name__)

_CONNECTION_POOL = None


def _initialize_connection_pool():
    global _CONNECTION_POOL
    try:
        connection_pool = redis.ConnectionPool(host="redis", port=6379, db=0)
        if connection_pool:
            _CONNECTION_POOL = connection_pool
            logger.info("Connection pool was created succesfully")
    except (redis.ConnectionError) as e:
        logger.error("Error while connecting to redis; %s", e)


def get_connection_pool():
    global _CONNECTION_POOL
    if _CONNECTION_POOL is None:
        _initialize_connection_pool()

    return _CONNECTION_POOL
