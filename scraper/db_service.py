from psycopg2 import extras

from scraper import db_init, models, utils

logger = utils.get_logger(__name__)
connection_pool = db_init.get_connection_pool()


def insert_parents(enterprise_number, parents: dict):
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    # Insert target.
    cursor.execute(
        """
        INSERT INTO cbe.entities (enterprise_number)
        VALUES (%s)
        RETURNING id;
        """,
        (enterprise_number,),
    )
    target_pk = cursor.fetchone()[0]

    # Insert entities and persons.
    unique_parents = dict()
    for parent_key, value in parents.items():
        if value not in unique_parents.values():
            unique_parents[parent_key] = value
    ids = dict()
    for parent_key, value in unique_parents.items():
        if isinstance(value, models.Entity):
            cursor.execute(
                """
                INSERT INTO cbe.entities (enterprise_number)
                VALUES (%s)
                RETURNING id;
                """,
                (value.enterprise_number,),
            )
            ids[parent_key] = cursor.fetchone()[0]
        if isinstance(value, models.Person):
            cursor.execute(
                """
                INSERT INTO cbe.persons (last_name, first_name)
                VALUES (%s, %s)
                RETURNING id;
                """,
                ((value.last_name, value.first_name)),
            )
            ids[parent_key] = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection_pool.putconn(connection)

    for parent_key, value in ids.items():
        parents[parent_key].id = value

    return target_pk


# Insert pivot entities.
def insert_children(target_pk: int, parents: dict, children: dict):
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    entities_persons_values_list = []
    entities_persons_sql = """INSERT INTO cbe.entities_persons (entity_id, person_id, function, start_date)
        VALUES %s
        """
    entities_entities_values_list = []
    entities_entities_sql = """
        INSERT INTO cbe.entities_entities (represented_entity_id, representative_entity_id, function, person_id, start_date)
        VALUES %s
        """
    for parent_key, parent_value in parents.items():
        if isinstance(parent_value, models.Entity):
            for child_key, child_value in children.items():
                if child_value.representative_entity == parent_value.enterprise_number:
                    person_id = parents[child_key].id
            entities_entities_values_list.append(
                (
                    target_pk,
                    parent_value.id,
                    children[parent_key].function,
                    person_id,
                    children[parent_key].start_date,
                )
            )
        elif isinstance(parent_value, models.Person):
            entities_persons_values_list.append(
                (
                    target_pk,
                    parent_value.id,
                    children[parent_key].function,
                    children[parent_key].start_date,
                )
            )
    extras.execute_values(cursor, entities_persons_sql, entities_persons_values_list)
    extras.execute_values(cursor, entities_entities_sql, entities_entities_values_list)

    connection.commit()
    cursor.close()
    connection_pool.putconn(connection)


# values_list = []
# values_list.append((value.last_name, value.first_name))
# sql = """INSERT INTO cbe.persons (last_name, first_name)
#     VALUES %s
#     ON CONFLICT ON CONSTRAINT persons_last_name_first_name_key DO NOTHING
#     RETURNING id;
#     """
# ids = extras.execute_values(cursor, sql, values_list, fetch=True)
