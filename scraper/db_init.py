import os

import dotenv
import psycopg2

from scraper import utils

logger = utils.get_logger(__name__)
dotenv.load_dotenv()

_CONNECTION_POOL = None


def _initialize_connection_pool():
    global _CONNECTION_POOL
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            20,
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DATABASE"),
        )
        if connection_pool:
            _CONNECTION_POOL = connection_pool
            logger.info("Connection pool was created successfully.")

    except (psycopg2.Error) as e:
        logger.info("Error while connecting to PostgreSQL: %s", e)


def get_connection_pool():
    global _CONNECTION_POOL
    if _CONNECTION_POOL is None:
        _initialize_connection_pool()

    return _CONNECTION_POOL


def close_connection_pool():
    global _CONNECTION_POOL
    # Close all the connections handled by the pool.
    if _CONNECTION_POOL is not None:
        _CONNECTION_POOL.closeall()
        logger.info("Connection pool has been closed.")
