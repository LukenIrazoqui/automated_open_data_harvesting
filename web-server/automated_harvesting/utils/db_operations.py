import psycopg2
from psycopg2 import sql
from django.conf import settings
from django.db import connection


def insert_row(insert_data):
    placeholders = ", ".join(["%s"] * len(insert_data['data']))

    insert_query = sql.SQL("""
            INSERT INTO {schame_name}.{table_name} ({fields})
            VALUES ({placeholders});
        """).format(
        schame_name=sql.Identifier(insert_data['schema']),
        table_name=sql.Identifier(insert_data['name']),
        fields=sql.SQL(', ').join(sql.Identifier(field) for field in insert_data['field_names']),
        placeholders=sql.SQL(placeholders)
    )

    with connection.cursor() as cursor:
        cursor.execute(insert_query, insert_data['data'])
    connection.commit()


def table_exists(table_data):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, (table_data['name'],))

        exists = cursor.fetchone()[0]

    if exists:
        print(f"Table {table_data['name']} exists")
    else:
        print(f"Table {table_data['name']} does not exist")

    return exists


def link_url_table(id, table_id):
    try:
        insert_data = {
            "schema": "public",
            "name": "url_table_mapping",
            "field_names": ["id_urls", "id_table_names"],
            "data": [id, table_id]
        }
        insert_row(insert_data)
    except Exception as e:
        print(f"Error linking URL ID {id} to table {table_id}: {e}")
        raise


def create_table(table_data):
    if not table_exists(table_data):
        print(f"Creating table {table_data['name']}")

        create_table_query = sql.SQL("""
                                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                                    id SERIAL PRIMARY KEY,
                                    {fields}
                                )
                            """).format(
            schema=sql.Identifier(table_data['schema']),
            table=sql.Identifier(table_data['name']),
            fields=sql.SQL(', ').join(sql.SQL("{} TEXT").format(sql.Identifier(field)) for field in table_data['field_names'])
        )

        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        connection.commit()


        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO table_names (name) 
                VALUES (%s) 
                RETURNING id
            """, (table_data['name'],))
            table_id = cursor.fetchone()[0]

        connection.commit()
        
        print(f"Table {table_data['name']} created successfully")

        link_url_table(table_data['id'], table_id)


def get_urls():
    sql_query = "SELECT id, name FROM urls;"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

    return rows
