import logging
from psycopg2 import sql
from django.db import connection
from ..models import TableNames, DynamicTableMapping

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('automated_harvesting.utils.db_operations')


def get_id(insert_data):
    select_query = sql.SQL("""
        SELECT id FROM {schema_name}.{table_name}
        WHERE {conditions}
        ORDER BY id DESC
        LIMIT 1;
    """).format(
        schema_name=sql.Identifier(insert_data['schema']),
        table_name=sql.Identifier(insert_data['name']),
        conditions=sql.SQL(' AND ').join(
            sql.SQL("{field} = %s").format(field=sql.Identifier(field))
            for field in insert_data['field_names']
        )
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(select_query, insert_data['data'])
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                raise ValueError("No row found after insertion")
    except Exception as e:
        logger.error(f"Error fetching id after insertion: {e}")
        raise


def row_exists(schema_name, table_name, unique_field_names, field_values):
    conditions = []
    for field_name in unique_field_names:
        conditions.append(sql.SQL("{field} = %s").format(field=sql.Identifier(field_name)))

    query = sql.SQL("""
        SELECT EXISTS (
            SELECT 1 FROM {schema_name}.{table_name}
            WHERE {conditions}
        )
    """).format(
        schema_name=sql.Identifier(schema_name),
        table_name=sql.Identifier(table_name),
        conditions=sql.SQL(" AND ").join(conditions)
    )

    with connection.cursor() as cursor:
        cursor.execute(query, field_values)
        return cursor.fetchone()[0]
    

def insert_row(insert_data):
    unique_field_names = insert_data['field_names']
    field_values = insert_data['data']

    if row_exists(insert_data['schema'], insert_data['name'], unique_field_names, field_values):
        print(f"Row with values {field_values} already exists. Skipping insertion.")
        return

    placeholders = ", ".join(["%s"] * len(field_values))

    insert_query = sql.SQL("""
        INSERT INTO {schema_name}.{table_name} ({fields})
        VALUES ({placeholders})
        RETURNING id;
    """).format(
        schema_name=sql.Identifier(insert_data['schema']),
        table_name=sql.Identifier(insert_data['name']),
        fields=sql.SQL(', ').join(sql.Identifier(field) for field in insert_data['field_names']),
        placeholders=sql.SQL(placeholders)
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, field_values)
            inserted_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Inserted row with values {field_values} successfully.")
        return inserted_id
    except Exception as e:
        logger.error(f"Error inserting row: {e}")
        connection.rollback()
        raise


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
        logger.info(f"Table {table_data['name']} exists")
    else:
        logger.info(f"Table {table_data['name']} does not exist")

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
        logger.info(f"Error linking URL ID {id} to table {table_id}: {e}")
        raise


def create_table(table_data):
    if not table_exists(table_data):
        logger.info(f"Creating table {table_data['name']}")

        schema_name = table_data['schema']
        table_name = table_data['name']
        field_names = table_data['field_names']
        id = table_data['id']

        if not field_names:
            raise ValueError("Field names list is empty, cannot create table.")

        try:
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                    id SERIAL PRIMARY KEY,
                    {field_definitions}
                );
            """).format(
                schema_name=sql.Identifier(schema_name),
                table_name=sql.Identifier(table_name),
                field_definitions=sql.SQL(', ').join(sql.SQL("{} TEXT").format(sql.Identifier(field)) for field in field_names)
            )

            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
            connection.commit()

            logger.info(f"Table {schema_name}.{table_name} created successfully with fields: {field_names}")

        except Exception as e:
            logger.error(f"Error creating table with table_data: {table_data}, error: {e}")
            raise

        logger.info(f"Adding {table_data['name']} to table_names")
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO table_names (name) 
                VALUES (%s) 
                RETURNING id
            """, (table_name,))
            
            table_id = cursor.fetchone()[0]

        connection.commit()
        
        logger.info(f"Linking {table_data['name']} to url : {table_data['id']}")

        link_url_table(table_data['id'], table_id)

    else :
        delete_query = sql.SQL("DELETE FROM {schema}.{table}").format(
            schema=sql.Identifier(table_data['schema']),
            table=sql.Identifier(table_data['name'])
        )

        with connection.cursor() as cursor:
            cursor.execute(delete_query)

        connection.commit()


def get_urls():
    sql_query = "SELECT id, name FROM urls;"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

    return rows


def is_table_dynamic(table_name):
    try:
        table = TableNames.objects.get(name=table_name)
        return table.dynamic
    except TableNames.DoesNotExist:
        return False
    

def get_dynamic_table_mappings(table_name):
    try:
        table = TableNames.objects.get(name=table_name)
        mappings = DynamicTableMapping.objects.filter(id_table_names=table)
        result = {
            'static_data_tables': [],
            'dynamic_data_tables': [],
        }

        for mapping in mappings:
            if mapping.id_static_data_table_names:
                result['static_data_tables'].append(mapping.id_static_data_table_names.name)
            if mapping.id_dynamic_data_table_names:
                result['dynamic_data_tables'].append(mapping.id_dynamic_data_table_names.name)

        return result
    
    except TableNames.DoesNotExist:
        return None
    

def get_column_names(table_name, schema_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' 
              AND table_schema = '{schema_name}'
        """)
        columns = cursor.fetchall()
    return [column[0] for column in columns]


def check_dynamic_and_get_columns(sheet_table_name):
    is_dynamic = is_table_dynamic(sheet_table_name)
    if is_dynamic:
        dynamic_mappings = get_dynamic_table_mappings(sheet_table_name)
        static_table_name = dynamic_mappings['static_data_tables']
        dynamic_table_name = dynamic_mappings['dynamic_data_tables']
        static_column_names = []
        dynamic_column_names = []

        if dynamic_mappings:
            static_column_names = get_column_names(dynamic_mappings['static_data_tables'], "data")
            dynamic_column_names = get_column_names(dynamic_mappings['dynamic_data_tables'], "data")

        if not static_column_names or not dynamic_column_names:
            is_dynamic = False
    else:
        static_column_names, dynamic_column_names, static_table_name, dynamic_table_name = None, None, None, None
    return is_dynamic, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name


def split_and_insert_dynamic_data(field_names, values, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name):
    static_data = {field: value for field, value in zip(field_names, values) if field in static_column_names}
    dynamic_data = {field: value for field, value in zip(field_names, values) if field in dynamic_column_names}

    static_insert_data = {
        "schema": "data",
        "name": static_table_name,
        "field_names": list(static_data.keys()),
        "data": list(static_data.values())
    }
    id = insert_row(static_insert_data)

    if id == None :
        id = get_id(static_insert_data)

    dynamic_insert_data = {
        "schema": "data",
        "name": dynamic_table_name,
        "field_names": list(dynamic_data.keys()) + ['static_id'],
        "data": list(dynamic_data.values()) + [id]
    }
    insert_row(dynamic_insert_data)