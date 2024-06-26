import logging
from dbfread import DBF
import tempfile
from ..db_operations import insert_row, create_table, is_table_dynamic, dynamic_mapping_columns
from .sanitize_names import sanitize_field_names

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_dbf(id, data, table_name):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(data)
            temp_file_path = temp_file.name

        dbf_data = DBF(temp_file_path)

        field_names = sanitize_field_names(dbf_data.field_names)

        table_data = {
            "schema": "data",
            "name": table_name,
            "field_names": field_names,
            "id" : id
        }

        try:
            create_table(table_data)
        except Exception as create_table_error:
            logger.error(f"Error occurred during table creation {table_name}: {create_table_error}")
            return

        is_dynamic = is_table_dynamic(table_name)
        if is_dynamic:
            static_column_names, dynamic_column_names = dynamic_mapping_columns(table_name, "data")
            if static_column_names == None or dynamic_column_names == None:
                is_dynamic = False

        try:
            for record in dbf_data:
                values = [str(record[field]) for field in dbf_data.field_names]

                if is_dynamic :
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

                else : 
                    insert_data = {
                        "schema": "data",
                        "name": table_name,
                        "field_names": field_names,
                        "data": values
                    }
                    insert_row(insert_data)


        except Exception as e:
            logger.error(f"Error occurred while inserting into table {table_name}: {e}")
            raise e
    except Exception as e:
        logger.error(f"An error occurred while processing DBF: {e}")
        raise e
