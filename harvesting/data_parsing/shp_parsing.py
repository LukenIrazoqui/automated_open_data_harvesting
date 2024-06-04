import os
import logging
from concurrent.futures import ThreadPoolExecutor
import shapefile
from io import BytesIO
from db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_shp(id, data, table_name):
    try:
        sf = shapefile.Reader(shp=BytesIO(data))

        field_names = sanitize_field_names(sf.fields[1:])

        if len(field_names) == 0:
            return

        table_data = {
            "schema": "data",
            "name": table_name,
            "field_names": field_names
        }

        create_table(table_data)
        link_url_table(id, table_name)

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for record in sf.records():
                values = [str(value) for value in record]

                insert_data = {
                    "schema": "data",
                    "name": table_name,
                    "field_names": field_names,
                    "data": values
                }
                executor.submit(insert_row, insert_data)

    except Exception as shp_process_error:
        logger.error(f"An error occurred while processing SHP: {shp_process_error}")
        raise shp_process_error
