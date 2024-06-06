import os
import logging
from concurrent.futures import ThreadPoolExecutor
from dbfread import DBF
import tempfile
from ..db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names

# Configure logging
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

            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                for record in dbf_data:
                    values = [str(record[field]) for field in dbf_data.field_names]

                    insert_data = {
                        "schema": "data",
                        "name": table_name,
                        "field_names": field_names,
                        "data": values
                    }
                    executor.submit(insert_row, insert_data)

        except Exception as e:
            logger.error(f"Error occurred while creating or inserting into table {table_name}: {e}")
            raise e
    except Exception as e:
        logger.error(f"An error occurred while processing DBF: {e}")
        raise e
