import logging
import shapefile
from io import BytesIO
from ..db_operations import insert_row, create_table, is_table_dynamic, dynamic_mapping_columns
from .sanitize_names import sanitize_field_names

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_and_insert_dynamic_data(table_name, field_names, values, static_column_names, dynamic_column_names):
    static_data = {field: value for field, value in zip(field_names, values) if field in static_column_names}
    dynamic_data = {field: value for field, value in zip(field_names, values) if field in dynamic_column_names}

    static_insert_data = {
        "schema": "data",
        "name": table_name,
        "field_names": list(static_data.keys()),
        "data": list(static_data.values())
    }
    insert_row(static_insert_data)

    dynamic_insert_data = {
        "schema": "data",
        "name": table_name,
        "field_names": list(dynamic_data.keys()),
        "data": list(dynamic_data.values())
    }
    insert_row(dynamic_insert_data)


def process_records(sf, field_names, table_name, is_dynamic, static_column_names, dynamic_column_names):
    for record in sf.records():
        values = [str(value) for value in record]

        if is_dynamic:
            split_and_insert_dynamic_data(table_name, field_names, values, static_column_names, dynamic_column_names)
        else:
            insert_data = {
                "schema": "data",
                "name": table_name,
                "field_names": field_names,
                "data": values
            }
            insert_row(insert_data)


def check_dynamic_and_get_columns(table_data):
    is_dynamic = is_table_dynamic(table_data)
    if is_dynamic:
        static_column_names, dynamic_column_names = dynamic_mapping_columns(table_data, "data")
        if not static_column_names or not dynamic_column_names:
            is_dynamic = False
    else:
        static_column_names, dynamic_column_names = None, None
    return is_dynamic, static_column_names, dynamic_column_names


def process_shp(id, data, table_name):
    try:
        sf = shapefile.Reader(shp=BytesIO(data))
        field_names = sanitize_field_names(sf.fields[1:])

        if len(field_names) == 0:
            return

        table_data = {
            "schema": "data",
            "name": table_name,
            "field_names": field_names,
            "id": id
        }

        try:
            create_table(table_data)
        except Exception as create_table_error:
            logger.error(f"Error creating table {table_name}: {create_table_error}")

        is_dynamic, static_column_names, dynamic_column_names = check_dynamic_and_get_columns(table_data)
        process_records(sf, field_names, table_name, is_dynamic, static_column_names, dynamic_column_names)

    except Exception as shp_process_error:
        logger.error(f"An error occurred while processing SHP: {shp_process_error}")
        raise shp_process_error
