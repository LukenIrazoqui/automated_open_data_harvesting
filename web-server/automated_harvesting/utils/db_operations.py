import psycopg2
from psycopg2 import sql
from django.conf import settings

def read_db_config():
    return {
        'database': settings.DATABASES['default']['NAME'],
        'username': settings.DATABASES['default']['USER'],
        'password': settings.DATABASES['default']['PASSWORD'],
        'hostname': settings.DATABASES['default']['HOST'],
        'port': settings.DATABASES['default']['PORT'],
    }

def get_connection():
    try:
        db_config = read_db_config()
        
        connection = psycopg2.connect(
            dbname=db_config['database'],
            user=db_config['username'],
            password=db_config['password'],
            host=db_config['hostname'],
            port=db_config['port']
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise


def insert_row(insert_data):
    try:

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

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(insert_query, insert_data['data'])
        connection.commit()

        print(f"Row data {insert_data['data']} inserted successfully into table {insert_data['name']}")
    except Exception as e:
        print(f"Error inserting row into table {insert_data['name']}: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def table_exists(table_data):
    try:
        connection = get_connection()
        cursor = connection.cursor()

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
    except Exception as e:
        print(f"Error checking if table {table_data['name']} exists: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def link_url_table(id, table_name):
    try:
        insert_data = {
            "schema": "public",
            "name": "url_table_mapping",
            "field_names": ["id_urls", "table_name"],
            "data": [id, table_name]
        }
        insert_row(insert_data)
    except Exception as e:
        print(f"Error linking URL ID {id} to table {table_name}: {e}")
        raise


def create_table(table_data):
    if not table_exists(table_data):
        print(f"Creating table {table_data['name']}")

        try:
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

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(create_table_query)

            connection.commit()
            print(f"Table {table_data['name']} created successfully")

            link_url_table(table_data['id'], table_data['name'])

        except Exception as e:
            print(f"Error creating table {table_data['name']}: {e}")
            raise


def get_urls():
    try:
        sql_query = "SELECT id, name FROM urls;"

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql_query)
        rows = cursor.fetchall()

        return rows
    except Exception as e:
        print(f"Error fetching URLs from the database: {e}")
        raise
    finally:
        cursor.close()
        connection.close()
