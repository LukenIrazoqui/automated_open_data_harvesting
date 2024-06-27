import logging
from dbfread import DBF
import tempfile
from ..db_operations import insert_row, create_table, check_dynamic_and_get_columns, split_and_insert_dynamic_data
from .sanitize_names import sanitize_field_names

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def insert_data_based_on_dynamic_status(table_name, field_names, values, is_dynamic, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name):
    if is_dynamic:
        split_and_insert_dynamic_data(field_names, values, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name)
    else:
        insert_data = {
            "schema": "data",
            "name": table_name,
            "field_names": field_names,
            "data": values
        }
        insert_row(insert_data)


def process_dbf_rows(dbf_data, table_name, field_names, is_dynamic, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name):
    for record in dbf_data:
        values = [str(record[field]) for field in dbf_data.field_names]
        insert_data_based_on_dynamic_status(table_name, field_names, values, is_dynamic, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name)


def setup_dbf_table(table_name, field_names, id):
    table_data = {
        "schema": "data",
        "name": table_name,
        "field_names": field_names,
        "id": id
    }

    try:
        create_table(table_data)
    except Exception as create_table_error:
        logger.error(f"Error occurred during table creation {table_name}: {create_table_error}")
        return False
    return True


def process_dbf(id, data, table_name):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(data)
            temp_file_path = temp_file.name

        dbf_data = DBF(temp_file_path)
        field_names = sanitize_field_names(dbf_data.field_names)

        if not setup_dbf_table(table_name, field_names, id):
            return

        is_dynamic, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name = check_dynamic_and_get_columns(table_name)

        try:
            process_dbf_rows(dbf_data, table_name, field_names, is_dynamic, static_column_names, dynamic_column_names, static_table_name, dynamic_table_name)
        except Exception as e:
            logger.error(f"Error occurred while inserting into table {table_name}: {e}")
            raise e
    except Exception as e:
        logger.error(f"An error occurred while processing DBF: {e}")
        raise e
