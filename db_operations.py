import configparser
import psycopg2
from psycopg2 import sql


def read_db_config(file_name='config.ini', section='postgresql'):
    parser = configparser.ConfigParser()
    parser.read(file_name)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {file_name} file')

    return db


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
        connection = get_connection()
        cursor = connection.cursor()

        placeholders = ", ".join(["%s"] * len(insert_data['data']))

        insert_query = sql.SQL("""
                INSERT INTO {schame_name}.{table_name} ({fields})
                VALUES ({placeholders})
                ON CONFLICT ({fields}) DO NOTHING;
            """).format(
            schame_name=sql.Identifier(insert_data['schema']),
            table_name=sql.Identifier(insert_data['name']),
            fields=sql.SQL(', ').join(sql.Identifier(field) for field in insert_data['field_names']),
            placeholders=sql.SQL(placeholders)
        )

        cursor.execute(insert_query, insert_data['data'])

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Row data {insert_data['data']} inserted successfully into table {insert_data['name']}")
    except Exception as e:
        print(f"Error inserting row into table {insert_data['name']}: {e}")
        raise


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

        cursor.close()
        connection.close()

        if exists:
            print(f"Table {table_data['name']} exists")
        else:
            print(f"Table {table_data['name']} does not exist")

        return exists
    except Exception as e:
        print(f"Error checking if table {table_data['name']} exists: {e}")
        raise


def link_url_table(id, table_name):
    try:
        insert_data = {
            "schema": "public",
            "name": "url_table_mapping",
            "field_names": ["url_id", "table_name"],
            "data": [id, table_name]
        }
        row_data = [id, table_name]
        field_names = ["url_id", "table_name"]
        insert_row(insert_data)
    except Exception as e:
        print(f"Error linking URL ID {id} to table {table_name}: {e}")
        raise


def create_table(table_data):
    if not table_exists(table_data):
        print(f"Creating table {table_data['name']}")
        connection = get_connection()
        cursor = connection.cursor()

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

            cursor.execute(create_table_query)

            # Creating composite unique constraint on all fields
            unique_constraint_query = sql.SQL("""
                                ALTER TABLE {schema}.{table}
                                ADD CONSTRAINT {constraint_name} UNIQUE ({fields})
                            """).format(
                schema=sql.Identifier(table_data['schema']),
                table=sql.Identifier(table_data['name']),
                constraint_name=sql.Identifier(f"unique_{table_data['name']}_fields"),
                fields=sql.SQL(', ').join(sql.Identifier(field) for field in table_data['field_names'])
            )

            cursor.execute(unique_constraint_query)

            connection.commit()
            print(f"Table {table_data['name']} created successfully")

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"Error creating table {table_data['name']}: {e}")
            cursor.close()
            connection.close()
            raise


def get_urls():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql_query = "SELECT id, name FROM urls;"

        cursor.execute(sql_query)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows
    except Exception as e:
        print(f"Error fetching URLs from the database: {e}")
        raise
