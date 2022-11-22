import pprint

import psycopg2
from psycopg2 import extras

from scraper import db_init, utils

logger = utils.get_logger(__name__)
_CONNECTION_POOL = db_init.get_connection_pool()


def insert_parents(parents: dict):

    connection = _CONNECTION_POOL.getconn()
    cursor = connection.cursor()
    pprint.pprint(parents)
    sql = """INSERT INTO cbe.persons (last_name, first_name)
        VALUES %s
        RETURNING id;
        """
    values_list = []
    values_list.append((parents[1].last_name, parents[1].first_name))
    ids = extras.execute_values(cursor, sql, values_list, fetch=True)
    connection.commit()
    cursor.close()
    _CONNECTION_POOL.putconn(connection)
    print(ids)
